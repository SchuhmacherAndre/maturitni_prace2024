import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import Image from "next/image";
import { buttonVariants } from "@/components/ui/button"
import Link  from "next/link";

export default function Settings() {
    return (
        <div className="overflow-x-hidden overflow-y-auto">

        

        <div className="flex justify-center items-center space-x-4 h-screen">
            <Button asChild variant="outline" className="h-64">
                <Link href="/">Back</Link>
            </Button>


            <Button asChild variant="outline" className="h-64 w-64 text-2xl">
            <Link href="/calibrate">Calibrate</Link>
            </Button>
            <Button asChild variant="outline" className="h-64 w-64 text-2xl">
            <Link href="/options">Options</Link>
            </Button>
        </div>
        </div>
    )

}