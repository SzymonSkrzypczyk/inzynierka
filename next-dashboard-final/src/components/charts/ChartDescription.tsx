import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";

interface ChartDescriptionProps {
    title?: string;
    children: React.ReactNode;
}

export function ChartDescription({ title = "Description", children }: ChartDescriptionProps) {
    return (
        <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="description" className="border-none">
                <AccordionTrigger className="py-2 text-sm font-medium hover:no-underline">
                    {title}
                </AccordionTrigger>
                <AccordionContent className="text-sm text-muted-foreground pb-4">
                    {children}
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    );
}
