// File:          comm.cpp
// Date:
// Description:
// Author:
// Modifications:

// You may need to add webots include files such as
// <webots/DistanceSensor.hpp>, <webots/Motor.hpp>, etc.
// and/or to add some other includes
#include <webots/Robot.hpp>
#include <webots/Motor.hpp>
#include <webots/Camera.hpp>
#include <webots/Emitter.hpp>
#include <webots/Receiver.hpp>
#include <opencv2/core/core.hpp>
#include <fstream>
#include <map>

#include "utilities.h"
#include "tcp_communication_looper.h"


#define TIMESTEP 250
#define MATMSG_END "E-N-D!"

// All the webots classes are defined in the "webots" namespace
using namespace webots;


class TCP_Caren_Controller : public Robot
{
    // IP and Buffersize load from Config
    std::string caren_ip_address;
    int read_buffer_size;
    // Ports loaded from the Config

    std::map<std::string, std::string> configMap;
    std::map<std::string, std::vector<webots::Motor*>> motorMap;
    std::map<std::string, webots::Camera*> cameraMap;
    std::map<std::string, webots::Receiver*> receiverMap;
    std::unique_ptr<ComLooper> comThread;

private:
    //****************************************************************************
    // This function has to be tailored to YOUR configFile !!!!!!!!!!!!!!!!!!!!!!!
    //****************************************************************************
    void initFromConfig()
    {
        if (configMap.find("camera_center_port_snd") != configMap.end() )
        {
            std::cout << "Initialize the Center Camera" << std::endl;
            //You define this identifier by yourself, but there cannot be duplicates!
            std::string cameraIdentifier = "camera_center";
            //The device names come from the webots world file
            cameraMap[cameraIdentifier] = getCamera("camera_center");

            if (configMap.find("camera_center_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(cameraIdentifier, std::stoi(configMap["camera_center_port_snd"]), configMap["cedar_ip"]);
            }
        }

        // TODO: add emitter-receiver pairs
        if (configMap.find("receiver_open_port_snd") != configMap.end() )
        {
            std::cout << "Initialize open receiver" << std::endl;
            //You define this identifier by yourself, but there cannot be duplicates!
            std::string receiverIdentifier = "open_receiver";
            //The device names come from the webots world file
            receiverMap[receiverIdentifier] = getReceiver("open_receiver");

            if (configMap.find("receiver_open_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(receiverIdentifier, std::stoi(configMap["receiver_open_port_snd"]), configMap["cedar_ip"]);
            }
        }


    }


    void sendCurrentMotorStatus()
    {
        for (auto const&[identifier, motorVector] : motorMap)
        {
            if (comThread->doesWriteSocketExist(identifier))
            {
                cv::Mat motorValues = cv::Mat::zeros(motorVector.size(), 1, CV_32F);
                for (std::vector<webots::Motor*>::size_type i = 0; i < motorVector.size(); i++)
                {
                    motorValues.at<float>(i, 0) = motorVector[i]->getTargetPosition();
                }

                comThread->setWriteMatrix(identifier,motorValues);
            }
        }
    }

    void readAndApplyMotorCommands()
    {
        for (auto const&[identifier, motorVector] : motorMap)
        {
            if (comThread->doesReadSocketExist(identifier))
            {
                cv::Mat commandMatrix = comThread->getReadCommandMatrix(identifier);
                if (commandMatrix.rows == (int) motorVector.size())
                {
                    for (std::vector<webots::Motor*>::size_type i = 0; i < motorVector.size(); i++)
                    {
                        motorVector[i]->setVelocity(1);
                        motorVector[i]->setPosition(commandMatrix.at<float>(i, 0));
                    }
                }
                else if(comThread->isReadSocketConnected(identifier) && commandMatrix.rows != 42) //I know this is kinda random, but I cannot init a Matrix with -1 and I also want to make sure that serializing went okay
                {
                    std::cout<<"Trying to Move: " << identifier  << ", but read a Matrix with " << commandMatrix.rows << " entries and we have only " << motorVector.size() << " motors." << std::endl;
                }
            }
        }
    }

    void sendCameraPictures()
    {
        for (auto const&[identifier, camera] : cameraMap)
        {
            if (comThread->doesWriteSocketExist(identifier))
            {
                cv::Mat pictureMat = getCameraPicture(camera);
                comThread->setWriteMatrix(identifier,pictureMat);
            }
        }

    }

    cv::Mat getCameraPicture(webots::Camera* cam)
    {
        int from_to[] =
                {0, 0, 1, 1, 2, 2}; // for mat conversion

        cv::Mat pictureMat(cam->getHeight(), cam->getWidth(), CV_8UC4,
                           const_cast<unsigned char *>(cam->getImage()));
        cv::Mat mat2 = cv::Mat(cam->getHeight(), cam->getWidth(), CV_8UC3);
        cv::mixChannels(&pictureMat, 1, &mat2, 1, from_to, 3); // kill the alpha channel

        return mat2;
    }

    std::map<std::string, std::string> readConfiguration(std::string configFilePath)
    {
        std::map<std::string, std::string> cMap;

        std::ifstream config_file(configFilePath);

        if (config_file.is_open())
        {
            std::string line;
            std::cout << "Read from Config:" << std::endl;
            while (std::getline(config_file, line))
            {
                if (line[0] != '#')
                {
                    std::vector<std::string> tokens;
                    split(line, ":", tokens);
                    if (tokens.size() == 2)
                    {
                        std::cout << "\t" << tokens[0] << " >> " << tokens[1] << std::endl;
                        cMap[tokens[0]] = tokens[1];
                    } else
                    {
                        std::cout << "Your Config File seems to be faulty. Each line should look like this >>identifier:value<< . Faulty line: " << line
                                  << std::endl;
                    }
                }
            }
        } else
        {
            std::cout << "ERROR! Could not open config file: " << configFilePath << std::endl;
        }

        config_file.close();


        return cMap;
    }


//Public functions
public:
    TCP_Caren_Controller(std::string
                         configFilePath) : Robot()
    {
        std::cout << "Create TCP_Caren_Controller with ConfigFile: " << configFilePath << std::endl;

        configMap = readConfiguration(configFilePath);
        //Create the Communication Thread
        comThread = std::make_unique<ComLooper>();

        auto camCenter = getCamera("camera_center");
        int camTimeStep = 4 * (int) this->getBasicTimeStep();
        camCenter->enable(camTimeStep);
    }

    ~TCP_Caren_Controller()
    {
        if (comThread->isRunning())
        {
            comThread->stop();
            comThread = nullptr;
        }
    }

    void run()
    {
        std::cout << "RUN! >CAREN TCP Controller< RUN!" << std::endl;

        initFromConfig();

        int timeStep = (int) this->getBasicTimeStep();

        comThread->run();

        while (this->step(timeStep) != -1)
        {
            readAndApplyMotorCommands();

            sendCurrentMotorStatus();

            sendCameraPictures();
            
            //ADD: save camera pic
            // cameraMap["camera_center"]->saveImage("home/minseok/D/webotpic.jpg", 10);
        }

        comThread->stop();
        comThread = nullptr;

    }

}; //End of Class


int main(int argc, char **argv)
{
    std::string configFileName = "default_config";
    if (argc > 1) //read configuration
    {
        configFileName = std::string(argv[1]);
    }
    // ADD: get handle to the camera
    // camera = getCamera("camera_center");


    // create the Robot instance.
    TCP_Caren_Controller *controller = new TCP_Caren_Controller(configFileName);
    controller->run();
    delete controller;
    return 0;
}
