import { GetServerSideProps } from "next";
import { getPlanetaryKIndex } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";
import { KpHeatmap } from "@/components/charts/KpHeatmap";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 500;
    const data = await getPlanetaryKIndex(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

export default function GeomagnetismPage({ data }: { data: any[] }) {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Geomagnetism</h2>
                <p className="text-muted-foreground">Planetary and Local K-index markers.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Planetary Kp — Time Series</CardTitle>
                    <ChartDescription>
                        <div className="space-y-2">
                            <p><strong>Description:</strong> A line chart showing the changes in the planetary geomagnetic index Kp over time.</p>
                            <p><strong>Purpose:</strong> To monitor global geomagnetic activity and identify periods of geomagnetic storms.</p>
                            <p><strong>Kp Scale:</strong></p>
                            <ul className="list-disc list-inside pl-4">
                                <li>0-1: Quiet conditions</li>
                                <li>2-4: Unsettled conditions</li>
                                <li>5: Geomagnetic storm (G1)</li>
                                <li>6: Moderate storm (G2)</li>
                                <li>7-9: Strong to extreme storm (G3-G5)</li>
                            </ul>
                        </div>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <TimeSeriesChart
                        data={data}
                        timeKey="timeTag"
                        lines={[
                            { key: 'kpIndex', name: 'Kp Index', color: 'var(--chart-1)' },
                            { key: 'estimatedKp', name: 'Estimated Kp', color: 'var(--chart-2)' }
                        ]}
                        yLabel="Kp Index"
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Heatmap — Kp Index Intensity</CardTitle>
                    <ChartDescription>
                        <p>Average Kp index values grouped by day and UTC hour. Color intensity corresponds to the Kp index value.</p>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <KpHeatmap data={data} />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Storm Events (Kp ≥ 5)</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead>
                                <tr className="border-b">
                                    <th className="pb-2 font-medium">Time (UTC)</th>
                                    <th className="pb-2 font-medium text-center">Kp Index</th>
                                    <th className="pb-2 font-medium text-center">G-Scale</th>
                                </tr>
                            </thead>
                            <tbody>
                                {data.filter(d => d.kpIndex >= 5).slice(0, 10).map((storm, i) => (
                                    <tr key={i} className="border-b">
                                        <td className="py-2">{new Date(storm.timeTag).toLocaleString()}</td>
                                        <td className="py-2 text-center font-bold text-red-600">{storm.kpIndex}</td>
                                        <td className="py-2 text-center">G-{storm.kpIndex - 4}</td>
                                    </tr>
                                ))}
                                {data.filter(d => d.kpIndex >= 5).length === 0 && (
                                    <tr>
                                        <td colSpan={3} className="py-4 text-center text-muted-foreground">No storm events in recent data.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
