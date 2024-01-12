"use client";

import { useEffect, useState } from 'react';
import { Button } from "@/components/ui/button";
import Link from 'next/link';

interface Dot {
  id: number;
  x: number;
  y: number;
  isDragging: boolean;
}

export default function Calibrate(){
    const [dots, setDots] = useState<Dot[]>([
        { id: 1, x: 100, y: 100, isDragging: false },
        { id: 2, x: 200, y: 100, isDragging: false },
        { id: 3, x: 100, y: 200, isDragging: false },
        { id: 4, x: 200, y: 200, isDragging: false },
      ]);
    
      const calculateDartboardRadius = (): number => {
        const distances = dots.map((dot) => Math.sqrt((dot.x - 200) ** 2 + (dot.y - 200) ** 2));
        const maxDistance = Math.max(...distances);
        return maxDistance + 20; // Add some padding
      };
    
      useEffect(() => {
        const handleMouseMove = (event: MouseEvent) => {
          const updatedDots = dots.map((dot) =>
            dot.isDragging ? { ...dot, x: event.pageX, y: event.pageY } : dot
          );
          setDots(updatedDots);
        };
    
        const handleMouseUp = () => {
          const updatedDots = dots.map((dot) => ({ ...dot, isDragging: false }));
          setDots(updatedDots);
        };
    
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
    
        return () => {
          document.removeEventListener('mousemove', handleMouseMove);
          document.removeEventListener('mouseup', handleMouseUp);
        };
      }, [dots]);
    
      const handleMouseDown = (id: number) => {
        const updatedDots = dots.map((dot) =>
          dot.id === id ? { ...dot, isDragging: true } : dot
        );
        setDots(updatedDots);
      };
    
      return (
        <div className="overflow-x-hidden overflow-y-auto">



            <div className="flex justify-center items-center space-x-4 h-screen">
            <Button asChild variant="outline" className="h-64">
                <Link href="/settings">Back</Link>
            </Button>
                <svg width="400" height="400" style={{ border: '1px solid #ccc' }}>
                {/* Draw Dartboard Circles */}
                <circle cx="200" cy="200" r={calculateDartboardRadius()} fill="white" />
                <circle cx="200" cy="200" r={calculateDartboardRadius() / 1.5} fill="#ffcc00" />
                <circle cx="200" cy="200" r={calculateDartboardRadius() / 2.5} fill="#009933" />
            
                {/* Draw Dartboard Sections */}
                {[0, 1, 2, 3].map((quadrant) => (
                    <line
                    key={quadrant}
                    x1="200"
                    y1="200"
                    x2={200 + calculateDartboardRadius() * Math.cos((quadrant * Math.PI) / 2)}
                    y2={200 + calculateDartboardRadius() * Math.sin((quadrant * Math.PI) / 2)}
                    stroke="#000"
                    />
                ))}
            
                {/* Draw Dots */}
                {dots.map((dot) => (
                    <circle
                    key={dot.id}
                    cx={dot.x}
                    cy={dot.y}
                    r={10}
                    fill="blue"
                    onMouseDown={() => handleMouseDown(dot.id)}
                    style={{ cursor: 'pointer' }}
                    />
                ))}
                </svg>
                </div>
                </div>
      );
}