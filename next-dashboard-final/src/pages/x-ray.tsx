import { GetServerSideProps } from "next";
import { getPrimaryXray } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 500;
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
    const processedData = data.map(d => ({
        ...d,
        flareClass: classifyFlux(d.flux)
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
                        data={processedData}
                        timeKey="timeTag"
                        lines={[
                            { key: 'flux', name: 'X-Ray Flux', color: '#ea580c' }
                        ]}
                        yLabel="Flux [W/m²]"
                        logScale={true}
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Solar Flare Classification</CardTitle>
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
                                {processedData.filter(d => d.flux >= 1e-6).slice(0, 10).map((flare, i) => (
                                    <tr key={i} className="border-b">
                                        <td className="py-2">{new Date(flare.timeTag).toLocaleString()}</td>
                                        <td className="py-2 text-center font-mono">{flare.flux.toExponential(2)}</td>
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
                                {processedData.filter(d => d.flux >= 1e-6).length === 0 && (
                                    <tr>
                                        <td colSpan={3} className="py-4 text-center text-muted-foreground">No moderate or strong flares in recent data.</td>
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
