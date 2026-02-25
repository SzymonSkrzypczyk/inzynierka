import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Brush } from "recharts";
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

    const showBrush = sortedData.length > 200;

    return (
        <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={sortedData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
                    <XAxis
                        dataKey={timeKey}
                        tickFormatter={(value) => format(new Date(value), "HH:mm")}
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        stroke="var(--muted-foreground)"
                        minTickGap={30}
                    />
                    <YAxis
                        scale={logScale ? "log" : "auto"}
                        domain={logScale ? ["auto", "auto"] : [0, "auto"]}
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                        stroke="var(--muted-foreground)"
                        label={yLabel ? { value: yLabel, angle: -90, position: 'insideLeft', style: { textAnchor: 'middle', fontSize: 12, fill: 'var(--muted-foreground)' } } : undefined}
                        tickFormatter={(val) => logScale ? val.toExponential(0) : val}
                    />
                    <Tooltip
                        labelFormatter={(value) => format(new Date(value), "yyyy-MM-dd HH:mm:ss")}
                        contentStyle={{
                            backgroundColor: 'var(--card)',
                            borderColor: 'var(--border)',
                            color: 'var(--foreground)',
                            borderRadius: '8px',
                            boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
                        }}
                    />
                    <Legend verticalAlign="top" height={36} />
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
                    {showBrush && (
                        <Brush
                            dataKey={timeKey}
                            height={30}
                            stroke="var(--chart-1)"
                            fill="var(--card)"
                            tickFormatter={(value) => format(new Date(value), "MM-dd")}
                        />
                    )}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
