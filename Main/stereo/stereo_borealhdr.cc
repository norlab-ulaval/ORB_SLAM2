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

#include <iostream>
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <chrono>
#include <stdio.h>
#include <dirent.h>

#include <opencv2/core/core.hpp>

#include <System.h>

using namespace std;

#define RESET "\033[0m"
#define BLACK "\033[30m"   /* Black */
#define RED "\033[31m"     /* Red */
#define GREEN "\033[32m"   /* Green */
#define YELLOW "\033[33m"  /* Yellow */
#define BLUE "\033[34m"    /* Blue */
#define MAGENTA "\033[35m" /* Magenta */
#define CYAN "\033[36m"    /* Cyan */
#define WHITE "\033[37m"   /* White */

void LoadImages(const string &strPathLeft, const string &strPathRight, vector<string> &vstrImageLeft,
                vector<string> &vstrImageRight, vector<double> &vTimeStamps);

int main(int argc, char **argv)
{
    if (argc != 6)
    {
        cerr << endl
             << "Usage: ./stereo_borealhdr path_to_vocabulary path_to_settings path_to_left_folder path_to_right_folder save_path" << endl;
        return 1;
    }

    // Retrieve paths to images
    vector<string> vstrImageLeft;
    vector<string> vstrImageRight;
    vector<double> vTimeStamp;
    LoadImages(string(argv[3]), string(argv[4]), vstrImageLeft, vstrImageRight, vTimeStamp);
    std::string savePath = argv[5];
    // Create save folder
    std::string command = "mkdir -p " + savePath;
    system(command.c_str());

    if (vstrImageLeft.empty() || vstrImageRight.empty())
    {
        cerr << "ERROR: No images in provided path." << endl;
        return 1;
    }

    if (vstrImageLeft.size() != vstrImageRight.size())
    {
        cerr << "ERROR: Different number of left and right images." << endl;
        return 1;
    }

    // Read rectification parameters
    cv::FileStorage fsSettings(argv[2], cv::FileStorage::READ);
    if (!fsSettings.isOpened())
    {
        cerr << "ERROR: Wrong path to settings" << endl;
        return -1;
    }

    cv::Mat K_l, K_r, P_l, P_r, R_l, R_r, D_l, D_r;
    fsSettings["LEFT.K"] >> K_l;
    fsSettings["RIGHT.K"] >> K_r;

    fsSettings["LEFT.P"] >> P_l;
    fsSettings["RIGHT.P"] >> P_r;

    fsSettings["LEFT.R"] >> R_l;
    fsSettings["RIGHT.R"] >> R_r;

    fsSettings["LEFT.D"] >> D_l;
    fsSettings["RIGHT.D"] >> D_r;

    int rows_l = fsSettings["LEFT.height"];
    int cols_l = fsSettings["LEFT.width"];
    int rows_r = fsSettings["RIGHT.height"];
    int cols_r = fsSettings["RIGHT.width"];

    if (K_l.empty() || K_r.empty() || P_l.empty() || P_r.empty() || R_l.empty() || R_r.empty() || D_l.empty() || D_r.empty() ||
        rows_l == 0 || rows_r == 0 || cols_l == 0 || cols_r == 0)
    {
        cerr << "ERROR: Calibration parameters to rectify stereo are missing!" << endl;
        return -1;
    }

    cv::Mat M1l, M2l, M1r, M2r;
    cv::initUndistortRectifyMap(K_l, D_l, R_l, P_l.rowRange(0, 3).colRange(0, 3), cv::Size(cols_l, rows_l), CV_32F, M1l, M2l);
    cv::initUndistortRectifyMap(K_r, D_r, R_r, P_r.rowRange(0, 3).colRange(0, 3), cv::Size(cols_r, rows_r), CV_32F, M1r, M2r);

    const int nImages = vstrImageLeft.size();

    // Create SLAM system. It initializes all system threads and gets ready to process frames.
    ORB_SLAM2::System SLAM(argv[1], argv[2], ORB_SLAM2::System::STEREO, false);

    // Vector for tracking time statistics
    vector<float> vTimesTrack;
    vTimesTrack.resize(nImages);

    cout << endl
         << "-------" << endl;
    cout << "Start processing sequence ..." << endl;
    cout << "Images in the sequence: " << nImages << endl
         << endl;

    // Main loop
    cv::Mat imLeft, imRight, imLeftRect, imRightRect;
    int count_map = 0;
    for (int ni = 0; ni < nImages; ni++)
    {
        // Read left and right images from file
        imLeft = cv::imread(vstrImageLeft[ni], CV_LOAD_IMAGE_UNCHANGED);
        imRight = cv::imread(vstrImageRight[ni], CV_LOAD_IMAGE_UNCHANGED);
        imLeft /= 16.0;
        imRight /= 16.0;
        imLeft.convertTo(imLeft, CV_8U);
        imRight.convertTo(imRight, CV_8U);

        if (imLeft.empty())
        {
            cerr << endl
                 << "Failed to load image at: "
                 << string(vstrImageLeft[ni]) << endl;
            return 1;
        }

        if (imRight.empty())
        {
            cerr << endl
                 << "Failed to load image at: "
                 << string(vstrImageRight[ni]) << endl;
            return 1;
        }

        cv::remap(imLeft, imLeftRect, M1l, M2l, cv::INTER_LINEAR);
        cv::remap(imRight, imRightRect, M1r, M2r, cv::INTER_LINEAR);

        // cv::imshow("Left", imLeftRect);
        // cv::imshow("Right", imRightRect);
        // cv::waitKey(0);

        double tframe = vTimeStamp[ni];

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t1 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t1 = std::chrono::monotonic_clock::now();
#endif

        // Pass the images to the SLAM system
        SLAM.TrackStereoCountMap(imLeftRect, imRightRect, tframe, count_map);
        cout << "Map number: " << count_map << endl;

#ifdef COMPILEDWITHC11
        std::chrono::steady_clock::time_point t2 = std::chrono::steady_clock::now();
#else
        std::chrono::monotonic_clock::time_point t2 = std::chrono::monotonic_clock::now();
#endif

        double ttrack = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1).count();

        vTimesTrack[ni] = ttrack;

        // Wait to load the next frame
        double T = 0;
        if (ni < nImages - 1)
            T = vTimeStamp[ni + 1] - tframe;
        else if (ni > 0)
            T = tframe - vTimeStamp[ni - 1];

        SLAM.SaveTrajectoryTUM(savePath + "/CameraTrajectory" + std::to_string(count_map) + ".txt");

        // if (ttrack < T)
        //     usleep((T - ttrack) * 1e6);
    }

    // Stop all threads
    SLAM.Shutdown();

    // Tracking time statistics
    sort(vTimesTrack.begin(), vTimesTrack.end());
    float totaltime = 0;
    for (int ni = 0; ni < nImages; ni++)
    {
        totaltime += vTimesTrack[ni];
    }
    cout << "-------" << endl
         << endl;
    cout << "median tracking time: " << vTimesTrack[nImages / 2] << endl;
    cout << "mean tracking time: " << totaltime / nImages << endl;

    // Save camera trajectory
    SLAM.SaveTrajectoryTUM(savePath + "/CameraTrajectory" + std::to_string(count_map) + ".txt");

    return 0;
}

void LoadImages(const string &strPathLeft, const string &strPathRight, vector<string> &vstrImageLeft,
                vector<string> &vstrImageRight, vector<double> &vTimeStamps)
{
    struct dirent *entry = nullptr;
    DIR *dp = nullptr;

    dp = opendir(strPathLeft.c_str());
    if (dp != nullptr)
    {
        while ((entry = readdir(dp)))
        {
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;
            std::string filename = entry->d_name;
            std::string timestampStr = filename.substr(0, filename.find_last_of('.'));
            vstrImageLeft.push_back(strPathLeft + "/" + filename);
            vTimeStamps.push_back(std::stod(timestampStr) / 1e9);
        }
    }
    else
    {
        perror("Couldn't open the directory");
    }

    // Try to match the left and right images
    std::vector<int> toRemove;
    for (int i = 0; i < vstrImageLeft.size(); i++)
    {
        // Check if the right image exists
        std::string imgName = vstrImageLeft[i].substr(vstrImageLeft[i].find_last_of('/') + 1);
        std::ifstream f(strPathRight + "/" + imgName);
        if (f.good())
        {
            vstrImageRight.push_back(strPathRight + "/" + imgName);
        }
        else
        {
            toRemove.push_back(i);
        }
    }

    // Ask the user if they want to remove the images that don't have a corresponding right image
    if (toRemove.size() > 0)
    {
        std::cout << YELLOW << "[WARNING] The following images were not in both folders:" << RESET << std::endl;
        for (int i = 0; i < toRemove.size(); i++)
        {
            std::cout << "  -> " << vstrImageLeft[toRemove[i]].substr(vstrImageLeft[i].find_last_of('/') + 1) << std::endl;
        }
        std::cout << "Do you want to remove them from the calculations? [y/n] ";
        char answer;
        std::cin >> answer;
        if (answer == 'n')
        {
            std::cout << "Exiting..." << std::endl;
            exit(0);
        }
    }

    // Remove the images that don't have a corresponding right image
    for (int i = toRemove.size() - 1; i >= 0; i--)
    {
        vstrImageLeft.erase(vstrImageLeft.begin() + toRemove[i]);
        vTimeStamps.erase(vTimeStamps.begin() + toRemove[i]);
    }

    closedir(dp);
}
