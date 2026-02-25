import { useMemo } from "react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface KpHeatmapProps {
    data: any[];
}

export function KpHeatmap({ data }: KpHeatmapProps) {
    const { heatmapData, dates, hours } = useMemo(() => {
        const pivot: Record<string, Record<number, number>> = {};
        const dateSet = new Set<string>();

        data.forEach(d => {
            const dateObj = new Date(d.timeTag);
            const dateStr = dateObj.toISOString().split('T')[0];
            const hour = dateObj.getUTCHours();

            dateSet.add(dateStr);
            if (!pivot[dateStr]) pivot[dateStr] = {};
            pivot[dateStr][hour] = d.kpIndex;
        });

        const sortedDates = Array.from(dateSet).sort().reverse();
        const sortedHours = Array.from({ length: 24 }, (_, i) => i);

        return { heatmapData: pivot, dates: sortedDates, hours: sortedHours };
    }, [data]);

    const getColor = (val: number | undefined) => {
        if (val === undefined) return "bg-muted/20";
        if (val >= 7) return "bg-red-700 dark:bg-red-600";
        if (val >= 5) return "bg-orange-600 dark:bg-orange-500";
        if (val >= 4) return "bg-yellow-500 dark:bg-yellow-400";
        if (val >= 2) return "bg-green-500 dark:bg-green-400";
        return "bg-blue-500 dark:bg-blue-400";
    };

    return (
        <div className="overflow-x-auto pb-4">
            <div className="min-w-[800px]">
                <div className="flex border-b pb-2 mb-2">
                    <div className="w-24 shrink-0 text-xs font-medium text-muted-foreground">Date</div>
                    <div className="flex flex-1">
                        {hours.map(h => (
                            <div key={h} className="flex-1 text-center text-[10px] text-muted-foreground">
                                {h.toString().padStart(2, '0')}
                            </div>
                        ))}
                    </div>
                </div>
                <div className="space-y-[2px]">
                    {dates.map(date => (
                        <div key={date} className="flex items-center h-6">
                            <div className="w-24 shrink-0 text-xs font-mono">{date}</div>
                            <div className="flex flex-1 h-full gap-[2px]">
                                {hours.map(hour => {
                                    const val = heatmapData[date]?.[hour];
                                    return (
                                        <TooltipProvider key={hour}>
                                            <Tooltip delayDuration={0}>
                                                <TooltipTrigger asChild>
                                                    <div className={`flex-1 rounded-sm ${getColor(val)}`} />
                                                </TooltipTrigger>
                                                <TooltipContent>
                                                    <div className="text-xs">
                                                        <p className="font-bold">{date} {hour}:00 UTC</p>
                                                        <p>Kp Index: {val ?? 'N/A'}</p>
                                                    </div>
                                                </TooltipContent>
                                            </Tooltip>
                                        </TooltipProvider>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            <div className="mt-4 flex flex-wrap gap-4 justify-center items-center text-[10px]">
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-sm bg-blue-500" /> <span>0-1 (Quiet)</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-sm bg-green-500" /> <span>2-3 (Unsettled)</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-sm bg-yellow-500" /> <span>4 (Unsettled)</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-sm bg-orange-600" /> <span>5-6 (Storm)</span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-3 h-3 rounded-sm bg-red-700" /> <span>7-9 (Extreme)</span>
                </div>
            </div>
        </div>
    );
}
