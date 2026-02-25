import { GetServerSideProps } from "next";
import { getPrimaryProtons } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 500;
    const data = await getPrimaryProtons(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

export default function ProtonsPage({ data }: { data: any[] }) {
    const energies = [...new Set(data.map(d => d.energy))].sort();

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Proton Radiation — Integral Fluxes</h2>
                <p className="text-muted-foreground">High-energy charged particles originating from the Sun and outer space.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Proton Flux by Energy Band</CardTitle>
                    <ChartDescription>
                        <div className="space-y-2">
                            <p><strong>Description:</strong> Temporal changes in proton flux in various energy bands.</p>
                            <p><strong>Purpose:</strong> To monitor radiation levels that can affect satellites, astronauts, and aviation.</p>
                            <p><strong>Interpretation:</strong> Sudden increases (Solar Particle Events) are often associated with powerful solar flares and coronal mass ejections.</p>
                        </div>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <TimeSeriesChart
                        data={data}
                        timeKey="timeTag"
                        lines={[
                            { key: 'flux', name: 'Integral Flux', color: '#f59e0b' }
                        ]}
                        yLabel="Flux [pfu]"
                        logScale={true}
                    />
                    <div className="mt-4 text-xs text-muted-foreground">
                        Showing aggregated flux data. Energy bands detected in this set: {energies.join(', ')}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
