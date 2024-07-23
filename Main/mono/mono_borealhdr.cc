/**
* This file is part of ORB-SLAM2.
*
* Copyright (C) 2014-2016 Raúl Mur-Artal <raulmur at unizar dot es> (University of Zaragoza)
* For more information see <https://github.com/raulmur/ORB_SLAM2>
*
* ORB-SLAM2 is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* ORB-SLAM2 is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with ORB-SLAM2. If not, see <http://www.gnu.org/licenses/>.
*/


#include<iostream>
#include<algorithm>
#include<fstream>
#include<chrono>
#include <stdio.h>
#include <dirent.h>

#include<opencv2/core/core.hpp>

#include<System.h>

using namespace std;

void LoadImages(const string &strImagePath, vector<string> &vstrImages, vector<double> &vTimeStamps);

int main(int argc, char **argv)
{
    if(argc != 5)
    {
        cerr << endl << "Usage: ./mono_tum path_to_vocabulary path_to_settings path_to_image_folder save_path" << endl;
        return 1;
    }

    // Retrieve paths to images
    vector<string> vstrImageFilenames;
    vector<double> vTimestamps;
    LoadImages(string(argv[3]), vstrImageFilenames, vTimestamps);

    std::string savePath = argv[4];
    // Create save folder
    std::string command = "mkdir -p " + savePath;
    system(command.c_str());

    int nImages = vstrImageFilenames.size();

    if(nImages<=0)
    {
        cerr << "ERROR: Failed to load images" << endl;
        return 1;
    }

    // Create SLAM system. It initializes all system threads and gets ready to process frames.
    ORB_SLAM2::System SLAM(argv[1],argv[2],ORB_SLAM2::System::MONOCULAR,false);

    // Vector for tracking time statistics
    vector<float> vTimesTrack;
    vTimesTrack.resize(nImages);

    cout << endl << "-------" << endl;
    cout << "Start processing sequence ..." << endl;
    cout << "Images in the sequence: " << nImages << endl << endl;

    // Main loop
    cv::Mat im;
    int count_map = 0;
    for(int ni=0; ni<nImages; ni++)
    {
        // Read image from file
        // im = cv::imread(vstrImageFilenames[ni],CV_LOAD_IMAGE_GRAYSCALE);
        im = cv::imread(vstrImageFilenames[ni],CV_LOAD_IMAGE_UNCHANGED);
        im /= 16.0;
        im.convertTo(im, CV_8U);

        double tframe = vTimestamps[ni];

        if(im.empty())
        {
            cerr << endl << "Failed to load image at: "
                 <<  vstrImageFilenames[ni] << endl;
            return 1;
        }

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t1 = std::chrono::monotonic_clock::now();
#endif

        // Pass the image to the SLAM system
        // SLAM.TrackMonocular(im,tframe);
        SLAM.TrackMonocularCountMap(im,tframe, count_map);
        cout << "Map number: " << count_map << endl;

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t2 = std::chrono::monotonic_clock::now();
#endif

        double ttrack= std::chrono::duration_cast<std::chrono::duration<double> >(t2 - t1).count();

        vTimesTrack[ni]=ttrack;

        // Wait to load the next frame
        double T=0;
        if(ni<nImages-1)
            T = vTimestamps[ni+1]-tframe;
        else if(ni>0)
            T = tframe-vTimestamps[ni-1];

        // if(ttrack<T)
        //     usleep((T-ttrack)*1e6);

        SLAM.SaveKeyFrameTrajectoryTUM(savePath + "/CameraTrajectory" + std::to_string(count_map) + ".txt");
    }

    // Stop all threads
    SLAM.Shutdown();

    // Tracking time statistics
    sort(vTimesTrack.begin(),vTimesTrack.end());
    float totaltime = 0;
    for(int ni=0; ni<nImages; ni++)
    {
        totaltime+=vTimesTrack[ni];
    }
    cout << "-------" << endl << endl;
    cout << "median tracking time: " << vTimesTrack[nImages/2] << endl;
    cout << "mean tracking time: " << totaltime/nImages << endl;

    // Save camera trajectory
    SLAM.SaveKeyFrameTrajectoryTUM(savePath + "/CameraTrajectory" + std::to_string(count_map) + ".txt");

    return 0;
}

// void LoadImages(const string &strImagePath, vector<string> &vstrImages, vector<double> &vTimeStamps)
// {
//     struct dirent *entry = nullptr;
//     DIR *dp = nullptr;

//     dp = opendir(strImagePath.c_str());
//     if (dp != nullptr) {
//         while ((entry = readdir(dp))) {
//             if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
//                 continue;
//             std::string filename = entry->d_name;
//             std::string timestampStr = filename.substr(0, filename.find_last_of('.'));
//             vstrImages.push_back(strImagePath + "/" + filename);
//             vTimeStamps.push_back(std::stod(timestampStr) / 1e9);
//         }
//     }
//     else {
//         perror ("Couldn't open the directory");
//     }

//     closedir(dp);
// }

void LoadImages(const string &strImagePath, vector<string> &vstrImages, vector<double> &vTimeStamps)
{
    struct dirent *entry = nullptr;
    DIR *dp = nullptr;

    dp = opendir(strImagePath.c_str());
    if (dp != nullptr)
    {
        while ((entry = readdir(dp)))
        {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            std::string filename = entry->d_name;
            std::string timestampStr = filename.substr(0, filename.find_last_of('.'));
            vstrImages.push_back(strImagePath + "/" + filename);
            vTimeStamps.push_back(std::stod(timestampStr) / 1e9);
        }
    }
    else
    {
        perror("Couldn't open the directory");
    }

    closedir(dp);
}