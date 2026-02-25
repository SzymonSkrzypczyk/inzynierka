import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { format } from "date-fns";

interface DataPoint {
    [key: string]: any;
}

interface TimeSeriesChartProps {
    data: DataPoint[];
    timeKey: string;
    lines: {
        key: string;
        name: string;
        color: string;
    }[];
    yLabel?: string;
    logScale?: boolean;
}

export function TimeSeriesChart({ data, timeKey, lines, yLabel, logScale }: TimeSeriesChartProps) {
    const sortedData = [...data].sort((a, b) =>
        new Date(a[timeKey]).getTime() - new Date(b[timeKey]).getTime()
    );

    return (
        <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sortedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
                    <XAxis
                        dataKey={timeKey}
                        tickFormatter={(value) => format(new Date(value), "HH:mm")}
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        stroke="hsl(var(--muted-foreground))"
                    />
                    <YAxis
                        scale={logScale ? "log" : "auto"}
                        domain={logScale ? ["auto", "auto"] : [0, "auto"]}
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        stroke="hsl(var(--muted-foreground))"
                        label={yLabel ? { value: yLabel, angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fontSize: 12, fill: 'hsl(var(--muted-foreground))' } } : undefined}
                    />
                    <Tooltip
                        labelFormatter={(value) => format(new Date(value), "yyyy-MM-dd HH:mm:ss")}
                        contentStyle={{
                            backgroundColor: 'hsl(var(--card))',
                            borderColor: 'hsl(var(--border))',
                            color: 'hsl(var(--foreground))',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                        }}
                    />
                    <Legend />
                    {lines.map((line) => (
                        <Line
                            key={line.key}
                            type="monotone"
                            dataKey={line.key}
                            name={line.name}
                            stroke={line.color}
                            dot={false}
                            activeDot={{ r: 4 }}
                            strokeWidth={2}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
