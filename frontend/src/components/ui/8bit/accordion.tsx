"use client";

import * as React from "react";

import * as AccordionPrimitive from "@radix-ui/react-accordion";

import { cn } from "@/lib/utils";

import {
 Accordion as ShadcnAccordion,
 AccordionContent as ShadcnAccordionContent,
 AccordionItem as ShadcnAccordionItem,
 AccordionTrigger as ShadcnAccordionTrigger,
} from "@/components/ui/accordion";

import "./styles/retro.css";

export interface BitAccordionItemProps
 extends React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item> {
 asChild?: boolean;
}

function AccordionItem({
 className,
 children,
 ...props
}: BitAccordionItemProps) {
 return (
  <ShadcnAccordionItem
   className={cn(
    "border-dashed border-b-4 border-foreground dark:border-ring relative",
    className
   )}
   {...props}
  >
   {children}
  </ShadcnAccordionItem>
 );
}

export interface BitAccordionTriggerProps
 extends React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Trigger> {
 font?: "normal" | "retro";
}

function AccordionTrigger({
 className,
 children,
 font,
 ...props
}: BitAccordionTriggerProps) {
 return (
  <ShadcnAccordionTrigger
   className={cn(font !== "normal" && "retro", className)}
   {...props}
  >
   {children}
  </ShadcnAccordionTrigger>
 );
}

export interface BitAccordionContentProps
 extends React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Content> {
 font?: "normal" | "retro";
}

function AccordionContent({
 className,
 children,
 font,
 ...props
}: BitAccordionContentProps) {
 return (
  <ShadcnAccordionContent
   className={cn(
    "overflow-hidden text-sm data-[state=closed]:animate-accordion-up",
    font !== "normal" && "retro",
    className
   )}
   {...props}
  >
   <div className="pb-4 pt-0">{children}</div>
  </ShadcnAccordionContent>
 );
}

const Accordion = ShadcnAccordion;

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent };