import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { buttonVariants } from "@/components/ui/button";
import Link from "next/link";
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
              <CardDescription className="text-xl">D20</CardDescription>
              <CardDescription className="text-xl">T18</CardDescription>
              <CardDescription className="text-xl">S11</CardDescription>
              <CardDescription className="text-xl">S05</CardDescription>
              <CardDescription className="text-xl">D20</CardDescription>
              <Button variant="outline" className=" mt-auto">Add Throw</Button>
              </Card>

              <CardHeader className="">
                  <CardTitle className="text-9xl">351</CardTitle>
              </CardHeader>

              

            </Card>
        </div>

        </Card>
      </div>
    </div>
  );
}
