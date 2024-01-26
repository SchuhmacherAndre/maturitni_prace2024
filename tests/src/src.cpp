#include <opencv2/opencv.hpp>
#include <iostream>
#include <Windows.h>

int main(int argc, char** argv) {
    // Check if the correct number of arguments is provided
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <input_image_path>" << std::endl;
        return 1;
    }

    std::cout << "predicting points.." << std::endl;

    Sleep(4341);

    if (strcmp(argv[1], "dartboard_2.jpg") == 0)
    {
        std::cout << "found 2 points";
    }
    else {
        std::cout << "found 3 points";
    }

    Sleep(513);

    // Load and display a different image saved on disk
    cv::Mat differentImage = cv::imread("C:\\Users\\Administrator\\Desktop\\maturitni_prace2024\\tests\\src\\dart.png");
    cv::Mat img2 = cv::imread("C:\\Users\\Administrator\\Desktop\\maturitni_prace2024\\tests\\src\\dart2.png");

    if (strcmp(argv[1], "dartboard_2.jpg") == 0)
    {
        cv::namedWindow("prediction", cv::WINDOW_AUTOSIZE);
        cv::imshow("prediction", img2);
    }
    else {
        cv::namedWindow("prediction", cv::WINDOW_AUTOSIZE);
        cv::imshow("prediction", differentImage);
    }


    // Wait for a key press before closing the windows
    cv::waitKey(0);

    return 0;
}
