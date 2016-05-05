#include "opencv2/opencv_modules.hpp"
#include <stdio.h>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/nonfree/features2d.hpp"

using namespace cv;
using namespace std;

//Function to find line points
void line_points(Vec2f line, Point *pt1, Point *pt2)
{
    float rho = line[0], theta = line[1];
    double a = cos(theta), b = sin(theta);
    double x0 = a*rho, y0 = b*rho;
    pt1->x = cvRound(x0 + 1000*(-b));
    pt1->y = cvRound(y0 + 1000*(a));
    pt2->x = cvRound(x0 - 1000*(-b));
    pt2->y = cvRound(y0 - 1000*(a)); 
    float Slope = (float)(pt2->y - pt1->y)/(float)(pt2->x - pt1->x);

    
    if(pt1->x < 0) 
    {           
        pt1->x = 0;
        pt1->y = pt2->y - ( Slope*(float)(pt2->x-pt1->x) );
    }

    if(pt1->x > fx) 
    {           
        pt1->x = fx;
        pt1->y = pt2->y - ( Slope*(float)(pt2->x-pt1->x) );
    }

    if(pt2->x < 0) 
    {           
        pt2->x = 0;
        pt2->y = pt1->y + ( Slope*(float)(pt2->x-pt1->x) );
    }

    if(pt2->x > fx) 
    {           
        pt2->x = fx;
        pt2->y = pt1->y + ( Slope*(float)(pt2->x-pt1->x) );
    }

    if(pt2->y > fy) 
    {           
        pt2->y = fy;
        pt2->x = pt1->x + ( (float)(pt2->y-pt1->y)/Slope );
    }

    if(pt2->y < 0) 
    {           
        pt2->y = 0;
        pt2->x = pt1->x + ( (float)(pt2->y-pt1->y)/Slope );
    }

    if(pt1->y < 0) 
    {           
        pt1->y = 0;
        pt1->x = pt2->x - ( (float)(pt2->y-pt1->y)/Slope );

 }

    if(pt1->y > fy) 
    {           
        pt1->y = fy;
        pt1->x = pt2->x - ( (float)(pt2->y-pt1->y)/Slope );
    }

    arrange_points(pt1,pt2);
           
}


int main()
{
    Mat pic, img, pic_bin;
  Mat rslt(pic.rows, pic.cols, CV_8UC3, Scalar(10,10,10));
    VideoCapture cap("out1.AVI");
    namedWindow("Control");    

    while (1)
    {
        cap >> pic;
        cvtColor(pic, img, CV_BGR2YUV);
        //imshow("original", pic);
        inRange(img, Scalar(99, 132, 81), Scalar(162, 164, 109), pic_bin);
        Canny(pic_bin, pic_bin, 50, 200, 3);
        cvtColor(pic_bin, rslt, CV_GRAY2BGR);
        vector<Vec2f> lines, group_lines;
        //erode(pic_bin, pic_bin, 5);
        HoughLines(pic_bin, lines, 1, CV_PI / 180, 100);

        int loop_no = lines.size();
        group_lines.clear();
        for( size_t i = 0; i < loop_no; i++ )
        {
            Point pt1, pt2;
            line_points(lines[i],&pt1,&pt2);
            float rho1 = lines[i][0], theta1 = lines[i][1];
            float meanRho = rho1;
            float meanTheta = theta1;
            int counter = 1;
            int flag_write = 0; 

            for (int j = 0; j < group_lines.size();j++)
            {
                Point pt3, pt4;
                line_points(group_lines[j],&pt3,&pt4);
                float rho2 = group_lines[j][0], theta2 = group_lines[j][1];
                if(  (norm(pt1 - pt3) + norm(pt2 - pt4)) < group_distance)
                {
                    flag_write = 1;
                    meanRho += rho2;
                    meanTheta += theta2;
                    counter++;
                }
            }           
            
            if(flag_write == 0)
            {
               group_lines.push_back(Vec2f(meanRho/counter,meanTheta/counter));          
            }
          
        }
        // Hough lines and filtering end

        // Display All lines
        for (size_t i = 0; i < lines.size(); i++)
        {
            float rho = lines[i][0], theta = lines[i][1];
            Point pt1, pt2;
            double a = cos(theta), b = sin(theta);
            double x0 = a*rho, y0 = b*rho;
            pt1.x = cvRound(x0 + 2000 * (-b));
            pt1.y = cvRound(y0 + 2000 * (a));
            pt2.x = cvRound(x0 - 2000 * (-b));
            pt2.y = cvRound(y0 - 2000 * (a));
            line(rslt, pt1, pt2, Scalar(0, 0, 255), 3, CV_AA);
        }
        //imshow("Converted", img);
        imshow("Control", rslt);
        // END Display All lines
        
        if (waitKey(30)==27)
            break;
    }
    return 0;
}