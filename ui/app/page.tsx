import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Image from "next/image";

// homepage... "main menu"
export default function Home() {
  return (
    <div className="overflow-x-hidden overflow-y-auto">
     

      <div className="flex justify-center items-center space-x-4 h-screen">
        <Button variant="outline" className="h-64 w-64 text-2xl">
          Play
        </Button>
        <Button variant="outline" className="h-64 w-64 text-2xl">
          Settings
        </Button>
        <Button variant="outline" className="h-64 w-64 text-2xl">
          Exit
        </Button>
      </div>
    </div>
  );
}
