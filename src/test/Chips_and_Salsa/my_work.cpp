
#include <iostream>
#include <string>
using namespace std;


int main(int argc, char const *argv[])
{

    struct Salsa {
        string name;
        int sold;
    };

    Salsa salsas[5] = {{"mild", 0}, {"medium", 0}, { "sweet", 0}, {"hot", 0},{"zesty", 0}};


    int totalSold = 0;
    int highestSold = -1;
    string highestSalsa = "";

    for (int i = 0; i < 5; i++)
    {
        int sold = 0;
        cout << "Enter jars of " <<  salsas[i].name + " sold: ";
        cin >> sold;
        cout << endl;

        totalSold += sold;

        if(sold > highestSold) {
            highestSold = sold;
            highestSalsa = salsas[i].name;
        }

    }

    cout << "Total sales: " << totalSold << "\nHighest selling salsa: " << highestSalsa << endl;

    return 0;
}
