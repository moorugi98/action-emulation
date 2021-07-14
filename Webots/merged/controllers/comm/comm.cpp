// File:          tcp_caren_controller.cpp
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
    int arm_port_rcv;
    int arm_port_snd;
    int head_port_rcv;
    int head_port_snd;
    int cam_port_snd;

    std::map<std::string, std::string> configMap;
    std::map<std::string, std::vector<webots::Motor*>> motorMap;
    std::map<std::string, webots::Camera*> cameraMap;
    std::unique_ptr<ComLooper> comThread;

private:
    //****************************************************************************
    // This function has to be tailored to YOUR configFile !!!!!!!!!!!!!!!!!!!!!!!
    //****************************************************************************
    void initFromConfig()
    {

        if (configMap.find("arm_port_snd") != configMap.end() || configMap.find("arm_port_rcv") != configMap.end())
        {
            std::cout << "Initialize the Arm!" << std::endl;

            //The motor names come from the webots world file
            std::vector<webots::Motor*> arm_motors;
            arm_motors.push_back(getMotor("arm_motor_0"));
            arm_motors.push_back(getMotor("arm_motor_1"));
            arm_motors.push_back(getMotor("arm_motor_2"));
            arm_motors.push_back(getMotor("arm_motor_3"));
            arm_motors.push_back(getMotor("arm_motor_4"));
            arm_motors.push_back(getMotor("arm_motor_5"));
            arm_motors.push_back(getMotor("arm_motor_6"));

            //You define this identifier by yourself, but there cannot be duplicates!
            std::string armIdentifier = "arm";
            motorMap[armIdentifier] = arm_motors;

            if (configMap.find("arm_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(armIdentifier, std::stoi(configMap["arm_port_snd"]), configMap["cedar_ip"]);
            }

            if (configMap.find("arm_port_rcv") != configMap.end())
            {
                comThread->addReadSocket(armIdentifier, std::stoi(configMap["arm_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
            }
        }

        if (configMap.find("head_port_snd") != configMap.end() || configMap.find("head_port_rcv") != configMap.end())
        {
            //The motor names come from the webots world file
            std::cout << "Initialize the Caren Head!" << std::endl;
            std::vector<webots::Motor*> head_motors;
            head_motors.push_back(getMotor("pan_camera_motor"));
            head_motors.push_back(getMotor("rotational_camera_motor"));

            //You define this identifier by yourself, but there cannot be duplicates!
            std::string headIdentifier = "head";
            motorMap[headIdentifier] = head_motors;

            if (configMap.find("head_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(headIdentifier, std::stoi(configMap["head_port_snd"]), configMap["cedar_ip"]);
            }

            if (configMap.find("head_port_rcv") != configMap.end())
            {
                comThread->addReadSocket(headIdentifier, std::stoi(configMap["head_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
            }
        }

        if (configMap.find("trunk_port_snd") != configMap.end() || configMap.find("trunk_port_rcv") != configMap.end())
        {
            std::cout << "Initialize the Caren Power Cube!" << std::endl;
            std::vector<webots::Motor*> cube_motors;
            cube_motors.push_back(getMotor("cube_motor"));

            std::string trunkIdentifier = "trunk";
            motorMap[trunkIdentifier] = cube_motors;

            if (configMap.find("trunk_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(trunkIdentifier, std::stoi(configMap["trunk_port_snd"]), configMap["cedar_ip"]);
            }

            if (configMap.find("trunk_port_rcv") != configMap.end())
            {
                comThread->addReadSocket(trunkIdentifier, std::stoi(configMap["trunk_port_rcv"]), std::stoi(configMap["read_buffer_size"]));
            }
        }

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

        if (configMap.find("caren_camera_port_snd") != configMap.end() )
        {
            std::cout << "Initialize the CAREN Camera" << std::endl;
            //You define this identifier by yourself, but there cannot be duplicates!
            std::string cameraIdentifier = "caren_camera";
            //The device names come from the webots world file
            cameraMap[cameraIdentifier] = getCamera("caren_camera");

            if (configMap.find("caren_camera_port_snd") != configMap.end())
            {
                comThread->addWriteSocket(cameraIdentifier, std::stoi(configMap["caren_camera_port_snd"]), configMap["cedar_ip"]);
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


    // create the Robot instance.
    TCP_Caren_Controller *controller = new TCP_Caren_Controller(configFileName);
    controller->run();
    delete controller;
    return 0;
}
