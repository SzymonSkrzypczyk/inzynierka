import { CartesianGrid, ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis, ZAxis } from "recharts";

interface FlareScatterChartProps {
    data: any[];
}

export function FlareScatterChart({ data }: FlareScatterChartProps) {
    const processedData = data.map(d => ({
        ...d,
        timeVal: new Date(d.timeTag).getTime(),
        timeStr: new Date(d.timeTag).toLocaleString(),
    }));

    const getColor = (flareClass: string) => {
        switch (flareClass) {
            case 'X': return '#ef4444'; // red-500
            case 'M': return '#f97316'; // orange-500
            case 'C': return '#3b82f6'; // blue-500
            case 'B': return '#854d0e'; // yellow-800 or brown
            case 'A': return '#22c55e'; // green-500
            default: return 'var(--muted-foreground)';
        }
    };

    // Grouping by flare class for multiple scatter series (allows legend control)
    const classes = ['A', 'B', 'C', 'M', 'X'];

    return (
        <div className="h-[350px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border)" />
                    <XAxis
                        type="number"
                        dataKey="timeVal"
                        name="Time"
                        domain={['auto', 'auto']}
                        tickFormatter={(unixTime) => new Date(unixTime).toLocaleDateString()}
                        fontSize={10}
                        stroke="var(--muted-foreground)"
                    />
                    <YAxis
                        type="number"
                        dataKey="maxFlux"
                        name="Flux"
                        scale="log"
                        domain={[1e-9, 1e-3]}
                        tickFormatter={(val) => val.toExponential(0)}
                        fontSize={10}
                        stroke="var(--muted-foreground)"
                        label={{ value: 'Flux [W/m²]', angle: -90, position: 'insideLeft', style: { fill: 'var(--muted-foreground)', fontSize: 10 } }}
                    />
                    <ZAxis type="number" range={[50, 50]} />
                    <Tooltip
                        content={({ active, payload }) => {
                            if (active && payload && payload.length) {
                                const d = payload[0].payload;
                                return (
                                    <div className="bg-card border p-2 rounded shadow text-xs">
                                        <p className="font-bold">{d.timeStr}</p>
                                        <p>Flux: {d.maxFlux.toExponential(2)} W/m²</p>
                                        <p>Class: <span className="font-bold" style={{ color: getColor(d.flareClass) }}>{d.flareClass}</span></p>
                                    </div>
                                );
                            }
                            return null;
                        }}
                    />
                    {classes.map(cls => (
                        <Scatter
                            key={cls}
                            name={`Class ${cls}`}
                            data={processedData.filter(d => d.flareClass === cls)}
                            fill={getColor(cls)}
                        />
                    ))}
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
}
