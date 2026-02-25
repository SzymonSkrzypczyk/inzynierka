import { GetServerSideProps } from "next";
import { getSolarRegions } from "@/lib/queries/space-weather";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TimeSeriesChart } from "@/components/charts/TimeSeriesChart";
import { ChartDescription } from "@/components/charts/ChartDescription";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { format } from "date-fns";

export const getServerSideProps: GetServerSideProps = async (context) => {
    const limit = context.query.limit ? parseInt(context.query.limit as string) : 500;
    const data = await getSolarRegions(limit);

    return {
        props: {
            data: JSON.parse(JSON.stringify(data)),
        },
    };
};

export default function SolarRegionsPage({ data }: { data: any[] }) {
    const dailyCountsMap = data.reduce((acc: any, d: any) => {
        const dateStr = format(new Date(d.observedDate), "yyyy-MM-dd");
        acc[dateStr] = (acc[dateStr] || 0) + 1;
        return acc;
    }, {});

    const dailyCounts = Object.entries(dailyCountsMap).map(([date, count]) => ({
        date,
        count
    })).sort((a, b) => a.date.localeCompare(b.date));

    const dailyAreaMap = data.reduce((acc: any, d: any) => {
        const dateStr = format(new Date(d.observedDate), "yyyy-MM-dd");
        if (!acc[dateStr]) acc[dateStr] = { sum: 0, count: 0 };
        acc[dateStr].sum += d.area;
        acc[dateStr].count += 1;
        return acc;
    }, {});

    const dailyArea = Object.entries(dailyAreaMap).map(([date, stats]: [string, any]) => ({
        date,
        meanArea: stats.sum / stats.count
    })).sort((a, b) => a.date.localeCompare(b.date));

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Active Solar Regions</h2>
                <p className="text-muted-foreground">Evolution and statistics of sunspot groups.</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Evolution of Active Region Area</CardTitle>
                    <ChartDescription>
                        <div className="space-y-2">
                            <p><strong>Description:</strong> Changes in the mean area of active solar regions over time.</p>
                            <p><strong>Interpretation:</strong> Area growth indicates development of magnetic activity and potentially higher probability of flares.</p>
                        </div>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <TimeSeriesChart
                        data={dailyArea}
                        timeKey="date"
                        lines={[
                            { key: 'meanArea', name: 'Mean Area [μhem]', color: '#16a34a' }
                        ]}
                        yLabel="Area [μhem]"
                    />
                </CardContent>
            </Card>

            <Card>
                <CardHeader>
                    <CardTitle>Daily Statistics of Active Regions</CardTitle>
                    <ChartDescription>
                        <p>Number of distinct active regions observed per day.</p>
                    </ChartDescription>
                </CardHeader>
                <CardContent>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={dailyCounts}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                                <XAxis dataKey="date" fontSize={12} tickLine={false} axisLine={false} />
                                <YAxis fontSize={12} tickLine={false} axisLine={false} />
                                <Tooltip />
                                <Bar dataKey="count" name="Region Count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
