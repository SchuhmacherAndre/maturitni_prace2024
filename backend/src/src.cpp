// src.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <mariadb/conncpp.hpp>



int main()
{

    sql::Driver* driver = sql::mariadb::get_driver_instance();
    sql::SQLString url("jdbc:mariadb://localhost:3306/test");
    sql::Properties properties({ {"user", "root"}, {"password", "andre"} });
    std::unique_ptr<sql::Connection> conn(driver->connect(url, properties));


    std::cout << "Hello World!\n";
}

