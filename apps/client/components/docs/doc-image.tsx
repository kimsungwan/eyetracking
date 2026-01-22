import Image from "next/image";
import { ZoomIn } from "lucide-react";

interface DocImageProps {
    src: string;
    alt: string;
}

export function DocImage({ src, alt }: DocImageProps) {
    return (
        <a
            href={src}
            target="_blank"
            rel="noopener noreferrer"
            className="group relative w-full h-48 bg-muted cursor-pointer overflow-hidden block"
        >
            <Image
                src={src}
                alt={alt}
                fill
                className="object-cover transition-transform duration-300 group-hover:scale-105"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300 flex items-center justify-center">
                <ZoomIn className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300 drop-shadow-md" />
            </div>
            <div className="absolute inset-0 border-2 border-transparent group-hover:border-primary transition-colors duration-300 pointer-events-none" />
        </a>
    );
}
