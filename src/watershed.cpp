#include <opencv2/opencv.hpp>
//#include <opencv2/core/utility.hpp>
//#include <opencv2/imgproc.hpp>
//#include <opencv2/imgcodecs.hpp>
//#include <opencv2/highgui.hpp>
#include <iostream>
using namespace std;
using namespace cv;


int main(int, char** argv)
{
    // Load the image
    Mat src = imread(argv[1]);
    // Check if everything was fine
    if (!src.data)
        return -1;
    // Show source image
    imshow("Source Image", src);
//    // Change the background from white to black, since that will help later to extract
//    // better results during the use of Distance Transform
//    for( int x = 0; x < src.rows; x++ ) {
//      for( int y = 0; y < src.cols; y++ ) {
//          if ( src.at<Vec3b>(x, y) == Vec3b(255,255,255) ) {
//            src.at<Vec3b>(x, y)[0] = 0;
//            src.at<Vec3b>(x, y)[1] = 0;
//            src.at<Vec3b>(x, y)[2] = 0;
//          }
//        }
//    }
//    // Show output image
//    imshow("Black Background Image", src);
    // Create a kernel that we will use for accuting/sharpening our image
    Mat kernel = (Mat_<float>(3,3) <<
            1,  1, 1,
            1, -8, 1,
            1,  1, 1); // an approximation of second derivative, a quite strong kernel
    // do the laplacian filtering as it is
    // well, we need to convert everything in something more deeper then CV_8U
    // because the kernel has some negative values,
    // and we can expect in general to have a Laplacian image with negative values
    // BUT a 8bits unsigned int (the one we are working with) can contain values from 0 to 255
    // so the possible negative number will be truncated
    Mat imgLaplacian;
    Mat sharp = src; // copy source image to another temporary one
    filter2D(sharp, imgLaplacian, CV_32F, kernel);
    src.convertTo(sharp, CV_32F);
    Mat imgResult = sharp - imgLaplacian;
    // convert back to 8bits gray scale
    imgResult.convertTo(imgResult, CV_8UC3);
    imgLaplacian.convertTo(imgLaplacian, CV_8UC3);
    // imshow( "Laplace Filtered Image", imgLaplacian );


    imshow( "New Sharped Image", imgResult );
    src = imgResult; // copy back
    // Create binary image from source image
    Mat bw;
    cvtColor(src, bw, CV_BGR2GRAY);
    threshold(bw, bw, 40, 255, CV_THRESH_BINARY | CV_THRESH_OTSU);
    imshow("Binary Image", bw);

    //find_connected components

 //   int nLabels = connectedComponents(bw, labelImage, 8);


    waitKey(0);
    return 0;
}
