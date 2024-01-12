"use client";

import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import * as React from "react";
import { MinusIcon, PlusIcon } from "@radix-ui/react-icons";

import { useState } from "react";

import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

import Link from "next/link";

export default function Picker() {
  const [isAlertVisible, setAlertVisible] = useState(false);

  const showAlert = () => {
    setAlertVisible(true);
  };

  const hideAlert = () => {
    setAlertVisible(false);
  };

  const [selectedButtons, setSelectedButtons] = useState<number[]>([]);

  const handleButtonClick = (buttonNumber: number) => {
    setSelectedButtons((prevSelected) => {
      if (prevSelected.includes(buttonNumber)) {
        // Button is already selected, so deselect it
        return prevSelected.filter((selected) => selected !== buttonNumber);
      } else {
        // Button is not selected, so select it
        return [buttonNumber];
      }
    });
    // Add any other logic you need when a button is clicked
  };

  const isButtonSelected = (buttonNumber: number) => {
    return selectedButtons.includes(buttonNumber);
  };

  return (
    <div className="overflow-x-hidden overflow-y-auto">
      <div className="flex justify-center items-center space-x-4 h-screen">
        <Button asChild variant="outline" className="h-64">
          <Link href="/">Back</Link>
        </Button>

        <Drawer>
          <DrawerTrigger asChild>
            <Button variant="outline" className="h-64 w-64 text-2xl">
              Select Gamemode
            </Button>
          </DrawerTrigger>
          <DrawerContent>
            <div className="mx-auto w-full max-w-sm">
              <DrawerHeader>
                <DrawerTitle>Select your preferred gamemode</DrawerTitle>
                <DrawerDescription>
                  Set up your ideal game here.
                </DrawerDescription>
              </DrawerHeader>
              <div className="p-4 pb-0">
                <div className="flex items-center justify-center space-x-2">
                  <div className="flex-1 text-center">
                    <div className="flex justify-center items-center space-x-2  ">
                      <Button
                        variant={isButtonSelected(1) ? "secondary" : "outline"}
                        onClick={() => handleButtonClick(1)}
                      >
                        501
                      </Button>
                      <Button
                        variant={isButtonSelected(2) ? "secondary" : "outline"}
                        onClick={() => handleButtonClick(2)}
                      >
                        301
                      </Button>
                      <Button
                        variant={isButtonSelected(3) ? "secondary" : "outline"}
                        onClick={() => handleButtonClick(3)}
                      >
                        101
                      </Button>
                    </div>
                  </div>

                  <div className=" mb-24"></div>
                </div>
              </div>
              <DrawerFooter>
                <div
                  style={{
                    position: "fixed",
                    bottom: 0,
                    right: 0,
                    padding: 15,
                  }}
                >
                  {isAlertVisible && (
                    <Alert variant="destructive" onAbort={hideAlert}>
                      <ExclamationTriangleIcon className="h-4 w-4" />
                      <AlertTitle>Error</AlertTitle>
                      <AlertDescription>
                        The camera hasn't been calibrated, please calibrate in
                        settings.
                      </AlertDescription>
                    </Alert>
                  )}
                </div>

                <Button onClick={showAlert}>Play</Button>
                <DrawerClose asChild>
                  <Button variant="outline" onClick={hideAlert}>
                    Cancel
                  </Button>
                </DrawerClose>
              </DrawerFooter>
            </div>
          </DrawerContent>
        </Drawer>
      </div>
    </div>
  );
}
