import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface HistogramChartProps {
    data: any[];
    dataKey: string;
    bins?: number;
    xLabel?: string;
    yLabel?: string;
    color?: string;
}

export function HistogramChart({ data, dataKey, bins = 20, xLabel, yLabel, color = "var(--chart-1)" }: HistogramChartProps) {
    if (!data.length) return null;

    const values = data.map(d => d[dataKey]).filter(v => typeof v === 'number');
    const min = Math.min(...values);
    const max = Math.max(...values);
    const range = max - min;
    const binSize = range / bins;

    const histogramData = Array.from({ length: bins }, (_, i) => {
        const binMin = min + i * binSize;
        const binMax = binMin + binSize;
        const count = values.filter(v => v >= binMin && (i === bins - 1 ? v <= binMax : v < binMax)).length;
        return {
            bin: `${binMin.toFixed(2)} - ${binMax.toFixed(2)}`,
            count,
            min: binMin,
            max: binMax
        };
    });

    return (
        <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={histogramData} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
                    <XAxis
                        dataKey="bin"
                        fontSize={10}
                        tickLine={false}
                        axisLine={false}
                        interval={Math.ceil(bins / 5)}
                        label={{ value: xLabel, position: 'insideBottom', offset: -10, fontSize: 12, fill: 'var(--muted-foreground)' }}
                    />
                    <YAxis
                        fontSize={10}
                        tickLine={false}
                        axisLine={false}
                        label={{ value: yLabel, angle: -90, position: 'insideLeft', fontSize: 12, fill: 'var(--muted-foreground)' }}
                    />
                    <Tooltip
                        cursor={{ fill: 'var(--muted)', opacity: 0.4 }}
                        contentStyle={{
                            backgroundColor: 'var(--card)',
                            borderColor: 'var(--border)',
                            color: 'var(--card-foreground)',
                            fontSize: '12px',
                            borderRadius: '8px',
                        }}
                    />
                    <Bar dataKey="count" fill={color} radius={[4, 4, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
