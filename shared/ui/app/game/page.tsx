"use client"

import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { buttonVariants } from "@/components/ui/button";
import Link from "next/link";
import { useState, useEffect } from "react";

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"

// homepage... "main menu"
export default function Game() {
  const [text, setText] = useState('');
  const [throws, setThrows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/getPoints');
        const response2 = await fetch('/api/getThrows');

        const jsonData = await response.json();
        const jsonData2 = await response2.json();

        setThrows(jsonData2.throws); // Assuming the API response contains an array named 'throws'
        setText(jsonData.t_pValue);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    const interval = setInterval(fetchData, 500); // Fetch data every 5 seconds
    fetchData(); // Fetch data initially when component mounts

    return () => clearInterval(interval); // Clean up interval on component unmount
  }, []);

  return (
    <div className="overflow-x-hidden overflow-y-auto">
      <div className="flex justify-center items-center space-x-4 h-screen">
      <Button asChild variant="outline" className="h-64">
          <Link href="/gamemode">Back</Link>
        </Button>

        <Card className=" h-3/4 w-3/4 text-2xl ">
            <CardHeader>
                <CardTitle>Active Dart Game</CardTitle>
                <CardDescription>Your dart game is currently active!</CardDescription>
            </CardHeader>

          <div className="justify-center flex items-center h-3/4">


            <Card className=" h-3/4 w-1/2 text-2xl  flex  ">

              <Card className="w-1/3 h-full text-l flex flex-col ">
              <CardTitle className="">previous throws</CardTitle>
              {loading ? (
                <p>Loading...</p>
              ) : (
                throws.map((throwValue, index) => (
                  <CardDescription key={index} className="text-xl">{throwValue}</CardDescription>
                ))
              )}
              <Button variant="outline" className=" mt-auto">Add Throw</Button>
              </Card>

              <CardHeader className="">
                  <CardTitle className="text-9xl">{text}</CardTitle>
              </CardHeader>

              

            </Card>
        </div>

        </Card>
      </div>
    </div>
  );
}
