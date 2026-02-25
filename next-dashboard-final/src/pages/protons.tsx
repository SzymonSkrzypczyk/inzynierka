import { GetServerSideProps } from "next";
import { getPrimaryProtons } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 2000;
    const data = await getPrimaryProtons(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

export default function ProtonsPage({ data }: { data: any[] }) {
    // Collect unique energies and sort them numerically if possible
    const energies = [...new Set(data.map(d => d.energy))].sort((a, b) => {
        const aNum = parseFloat(a.replace(/[^\d.]/g, '')) || 0;
        const bNum = parseFloat(b.replace(/[^\d.]/g, '')) || 0;
        return aNum - bNum;
    });

    // Pivot data: Group by timeTag
    const pivotedDataMap = data.reduce((acc: any, d: any) => {
        const time = d.timeTag;
        if (!acc[time]) {
            acc[time] = { timeTag: time };
        }
        acc[time][d.energy] = d.flux;
        return acc;
    }, {});

    const pivotedData = (Object.values(pivotedDataMap) as any[]).sort((a: any, b: any) =>
        new Date(a.timeTag).getTime() - new Date(b.timeTag).getTime()
    );

    const lines = energies.map((energy, i) => ({
        key: energy,
        name: energy,
        color: `var(--chart-${(i % 5) + 1})`
    }));

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
                        data={pivotedData}
                        timeKey="timeTag"
                        lines={lines}
                        yLabel="Flux [pfu]"
                        logScale={true}
                    />
                    <div className="mt-4 text-xs text-muted-foreground">
                        Showing data across {energies.length} energy bands: {energies.join(', ')}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
