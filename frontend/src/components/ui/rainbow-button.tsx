"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface RainbowButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export function RainbowButton({
  children,
  className,
  ...props
}: RainbowButtonProps) {
  return (
    <button
      className={cn(
        "group relative inline-flex h-11 animate-rainbow cursor-pointer items-center justify-center rounded-xl border-0 bg-[length:200%] px-8 py-2 font-medium text-white transition-colors [background-image:linear-gradient(90deg,#00f2ff_0%,#00d2ff_25%,#00f2ff_50%,#00d2ff_75%,#00f2ff_100%)] hover:brightness-110 active:scale-95 disabled:pointer-events-none disabled:opacity-50",
        className,
      )}
      {...props}
    >
      <span className="relative z-10 flex items-center gap-2">{children}</span>
      <div
        className={cn(
          "absolute inset-0 -z-10 h-full w-full animate-rainbow rounded-xl bg-[length:200%] opacity-30 blur-lg transition-opacity group-hover:opacity-50 [background-image:linear-gradient(90deg,#00f2ff_0%,#00d2ff_25%,#00f2ff_50%,#00d2ff_75%,#00f2ff_100%)]",
        )}
      />
    </button>
  );
}
