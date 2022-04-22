#include <iostream>
#include <vector>


/*
    This code finds an optimal path to avoid a detected object
    in a discrete time interval
    

*/


// Argc: Number of objects
// 
// Argv: Position of the object
// argv[i] = [r, theta_left, theta_right]
#define N_DATA_ARGV 3
// r: distance to the center of the object
// theta: angle [-90, 90] to the object
// left/right is the furthest position in each direction

// Robot Paramaters 
#define MIN_BRAKEING_DISTANCE 0.2500 // "breaking distance" in meters
#define MAX_ACCELLERATION_RATE
#define MAX_TURN_ANGLE 45 // 45 degrees
#define MAX_CENTRIFUGAL_FORCE 3 // N of force before the robot tips over
#define TIME_INTERVAL 3.0 // seconds 



class Object
{
    private:
        double r;
        double theta_left;
        double theta_right;
    public:
        Object(double new_r = 0, double new_theta_left = 0, double new_theta_right = 0)
        {
            r           = new_r;
            theta_left  = new_theta_left;
            theta_right = new_theta_right;
        }
        ~Object(){}
};








// Calculate reachable set given current paramaters
double* direction_vector(Object* objects)
{
    // input: 2d array of objects where object[i] = [r, theta, width]




    return 0;
} 






int main(int argc, char **argv) 
{
    std::vector<Object> objects;
    
    // Add objects from input to an array of "Object" class items 
    for(int i = 0; i < argc; i++)
    {
        Object temp_obj(argv[i][0], argv[i][1], argv[i][2]);
        objects.push_back(temp_obj);
    }
    




    
    return 0;
}

