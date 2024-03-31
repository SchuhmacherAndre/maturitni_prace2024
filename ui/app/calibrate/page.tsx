"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import Image from "next/image";
import $ from "jquery"


export default function Calibrate() {

  useEffect(() => {
    let isDragging = false;
    let currentCrosshair: JQuery<HTMLElement>;
    let zoom = 3;
    var img, glass, w: any, h: any, bw: any;
    var imag = document.getElementById("myimage")!;
    

    for (let i = 1; i < 5; i++) {
      glass = document.getElementById("glass"+i)!;
      /* Set background properties for the magnifier glass: */
      glass.style.backgroundImage = "url('" + "/IMG_0001.jpg" + "')";
      glass.style.backgroundRepeat = "no-repeat";
      glass.style.backgroundSize = (imag.clientWidth * zoom) + "px " + (imag.clientHeight * zoom) + "px";
      bw = 3;
      w = glass.offsetWidth / 2;
      h = glass.offsetHeight / 2;
    }

    $(".img-magnifier-glass").on("mousedown touchstart", function(e: any) {
      isDragging = true;
      currentCrosshair = $(this) as JQuery<HTMLElement>;

      e.preventDefault(); // Prevent default touch behavior
    });

    $(document).on("mousemove touchmove", function(e: any) {
      if (isDragging) {
          let containerOffset = $(".img-magnifier-container").offset()!;

          let test = $("#myimage").offset()!;
          let clientX, clientY;

          if (e.type === "touchmove") {
              clientX = e.originalEvent.touches[0].clientX;
              clientY = e.originalEvent.touches[0].clientY;
          } else {
              clientX = e.clientX;
              clientY = e.clientY;
          }
          
          let xPos = clientX - test.left - 50; // Adjust for crosshair size
          let yPos = clientY -  containerOffset.top - 50; // Adjust for crosshair size

 
          currentCrosshair.css({ left: xPos, top: yPos });


          var pos, x, y;
          /* Prevent any other actions that may occur when moving over the image */
          e.preventDefault();
                /* Get the cursor's x and y positions: */
           x = clientX - test.left - 40; // Adjust for crosshair size
           y = clientY -  test.top - 25; 

          /* Prevent the magnifier glass from being positioned outside the image: */
          currentCrosshair.css({
            backgroundPosition: "-" + ((x * zoom) - w + bw) + "px -" + ((y * zoom) - h + bw)  + "px"
        });
      }
    });

    $(document).on("mouseup touchend", function(e: any) {
        if (isDragging) {
            let img = document.getElementById("myimage") as HTMLImageElement;
            let containerOffset = $(".img-magnifier-container").offset();
            let clientX, clientY;
            if (e.type === "touchend") {
                clientX = e.originalEvent.changedTouches[0].clientX;
                clientY = e.originalEvent.changedTouches[0].clientY;
            } else {
                clientX = e.clientX;
                clientY = e.clientY;
            }
            let xPos = ((clientX - 25) - img.offsetLeft) * (img.naturalWidth / img.width);
            let yPos = ((clientY - 25) - img.offsetTop) * (img.naturalHeight / img.height);
            console.log("Image Coordinates: " + currentCrosshair.attr("id"), { x: xPos + 30, y: yPos });
            isDragging = false;
        }
    }); 

  }, []);
    



  return (
    <div className="overflow-x-hidden overflow-y-auto">
      <div className="flex justify-center items-center space-x-4 h-screen">
      <Button asChild variant="outline" className="h-64">
                <Link href="/settings">Back</Link>
            </Button>

        <div className="img-magnifier-container">
          <div className="img-magnifier-glass left-72 top-96" id="glass4"><a className="cross font-light">+</a><div className="floating-word">Fourth</div></div>
          <div className="img-magnifier-glass left-48 top-96" id="glass3"><a className="cross font-light">+</a><div className="floating-word">Third</div></div>
          <div className="img-magnifier-glass left-24 top-96" id="glass2"><a className="cross font-light">+</a><div className="floating-word">Second</div></div>
          <div className="img-magnifier-glass top-96" id="glass1"><a className="cross font-light">+</a><div className="floating-word">First</div></div>
        </div>
          
          


        <img className="" id="myimage" src="/IMG_0001.jpg" style={{ width: '50%' }} alt="dartboard"></img>




      </div>
      <style jsx>{`
        * {box-sizing: border-box;}

        .img-magnifier-container {
          position: relative;
        }

        .img-magnifier-glass {
          position: absolute;
          border: 3px solid #000;
          border-radius: 50%;
          display: flex;
          justify-content: center; /* horizontally center */
          align-items: center; /* vertically center */
          cursor: crosshair;
          /* Set the size of the magnifier glass: */
          width: 50px;
          height: 50px;
        }

        .cross {
            cursor: crosshair;
            font-size: 36px; /* Adjust font size as needed */
            color: cyan;
            
        }

        .floating-word {
          position: absolute;
          top: -30px; /* Adjust top position */
          left: 50%; /* Adjust left position */
          transform: translateX(-50%); /* Center horizontally */
          font-size: 32px; /* Adjust font size as needed */
          color: white; /* Adjust color as needed */
        }


      `}</style>
    </div>

  );
}
