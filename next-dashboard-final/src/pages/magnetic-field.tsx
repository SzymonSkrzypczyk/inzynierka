import { GetServerSideProps } from "next";
import { getDscovrMag } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 500;
    const data = await getDscovrMag(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

export default function MagneticFieldPage({ data }: { data: any[] }) {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Interplanetary Magnetic Field (DSCOVR)</h2>
                <p className="text-muted-foreground">Components of the solar wind magnetic field measured at L1.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Magnetic Field Components (GSM)</CardTitle>
                    <ChartDescription>
                        <div className="space-y-2">
                            <p><strong>Description:</strong> Temporal changes in the magnetic field components measured by DSCOVR.</p>
                            <p><strong>Variables:</strong></p>
                            <ul className="list-disc list-inside pl-4">
                                <li><strong>Bt</strong>: Total magnetic field magnitude.</li>
                                <li><strong>Bx, By, Bz</strong>: Vector components in the Geocentric Solar Magnetospheric (GSM) system.</li>
                            </ul>
                            <p><strong>Interpretation:</strong> Negative (southward) Bz values are critical for geomagnetic storm initiation as they allow for reconnection with Earth's magnetic field.</p>
                        </div>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <TimeSeriesChart
                        data={data}
                        timeKey="timeTag"
                        lines={[
                            { key: 'bt', name: 'Bt (Total)', color: 'var(--chart-1)' },
                            { key: 'bxGsm', name: 'Bx (GSM)', color: 'var(--chart-2)' },
                            { key: 'byGsm', name: 'By (GSM)', color: 'var(--chart-3)' },
                            { key: 'bzGsm', name: 'Bz (GSM)', color: 'var(--chart-4)' }
                        ]}
                        yLabel="Induction [nT]"
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Bz Component Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="h-[200px] flex items-center justify-center text-muted-foreground italic">
                        Statistical distribution of Bz values (Histogram) would be implemented here.
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
