import { GetServerSideProps } from "next";
import { getPrimaryXray } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";
import { FlareScatterChart } from "@/components/charts/FlareScatterChart";
import { HistogramChart } from "@/components/charts/HistogramChart";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 1000;
    const data = await getPrimaryXray(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

function classifyFlux(v: number): string {
    if (v >= 1e-4) return 'X';
    if (v >= 1e-5) return 'M';
    if (v >= 1e-6) return 'C';
    if (v >= 1e-7) return 'B';
    return 'A';
}

export default function XrayPage({ data }: { data: any[] }) {
    // Collect unique satellites
    const satellites = [...new Set(data.map(d => `GOES-${d.satellite}`))].sort();

    // Pivot data: Group by timeTag
    const pivotedDataMap = data.reduce((acc: any, d: any) => {
        const time = d.timeTag;
        const satName = `GOES-${d.satellite}`;
        if (!acc[time]) {
            acc[time] = { timeTag: time };
        }
        acc[time][satName] = d.flux;
        // For classification, we use the max flux at this time point if multiple sats exist
        acc[time].maxFlux = Math.max(acc[time].maxFlux || 0, d.flux);
        return acc;
    }, {});

    const pivotedData = (Object.values(pivotedDataMap) as any[]).sort((a: any, b: any) =>
        new Date(a.timeTag).getTime() - new Date(b.timeTag).getTime()
    ).map(d => ({
        ...d,
        flareClass: classifyFlux(d.maxFlux)
    }));

    const lines = satellites.map((sat, i) => ({
        key: sat,
        name: sat,
        color: `var(--chart-${(i % 5) + 1})`
    }));

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Solar X-Ray Radiation</h2>
                <p className="text-muted-foreground">Monitoring solar flares and hard/soft X-ray emissions.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>X-Ray Flux by Satellite</CardTitle>
                    <ChartDescription>
                        <div className="space-y-2">
                            <p><strong>Description:</strong> Temporal changes in X-ray flux emitted by the Sun.</p>
                            <p><strong>Bands:</strong> Hard X-rays (energy {">"} 50 keV) and Soft X-rays (energy {"<"} 10 keV).</p>
                            <p><strong>Interpretation:</strong> Sudden spikes indicate solar flares, which are classified by peak flux.</p>
                        </div>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <TimeSeriesChart
                        data={pivotedData}
                        timeKey="timeTag"
                        lines={lines}
                        yLabel="Flux [W/m²]"
                        logScale={true}
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Solar Flare Classification Scatter</CardTitle>
                    <ChartDescription>
                        <p>A scatter plot showing all X-ray flux measurements classified by solar flare class.</p>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <FlareScatterChart data={pivotedData} />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Solar Flare Classification Table</CardTitle>
                    <ChartDescription>
                        <p>Classification based on peak X-ray flux in the 0.1–0.8 nm range.</p>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead>
                                <tr className="border-b">
                                    <th className="pb-2 font-medium">Time (UTC)</th>
                                    <th className="pb-2 font-medium text-center">Flux [W/m²]</th>
                                    <th className="pb-2 font-medium text-center">Class</th>
                                </tr>
                            </thead>
                            <tbody>
                                {pivotedData.filter((d: any) => d.maxFlux >= 1e-6).slice(0, 10).map((flare: any, i: number) => (
                                    <tr key={i} className="border-b">
                                        <td className="py-2">{new Date(flare.timeTag).toLocaleString()}</td>
                                        <td className="py-2 text-center font-mono">{flare.maxFlux.toExponential(2)}</td>
                                        <td className="py-2 text-center font-bold">
                                            <span className={
                                                flare.flareClass === 'X' ? 'text-red-600' :
                                                    flare.flareClass === 'M' ? 'text-orange-500' :
                                                        'text-blue-500'
                                            }>
                                                {flare.flareClass}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                                {pivotedData.filter((d: any) => d.maxFlux >= 1e-6).length === 0 && (
                                    <tr>
                                        <td colSpan={3} className="py-4 text-center text-muted-foreground">No moderate or strong flares in recent data.</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>X-Ray Flux Distribution</CardTitle>
                    <ChartDescription>
                        <p>Statistical distribution of X-ray flux values. Shift to the right indicates increased solar activity.</p>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <HistogramChart
                        data={pivotedData}
                        dataKey="maxFlux"
                        bins={30}
                        xLabel="Flux [W/m²]"
                        yLabel="Count"
                        color="var(--chart-3)"
                    />
                </CardContent>
            </Card>
        </div>
    );
}
