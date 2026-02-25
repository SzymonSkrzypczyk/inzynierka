import { GetServerSideProps } from "next";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { getPlanetaryKIndex, getDscovrMag, getPrimaryProtons, getPrimaryXray } from "@/lib/queries/space-weather";
import { Activity, Magnet, Zap, Sun } from "lucide-react";

export const getServerSideProps: GetServerSideProps = async () => {
  const [kp, mag, protons, xray] = await Promise.all([
    getPlanetaryKIndex(1),
    getDscovrMag(1),
    getPrimaryProtons(1),
    getPrimaryXray(1),
  ]);

  return {
    props: {
      latestData: JSON.parse(
        JSON.stringify({
          kp: kp[0] || null,
          mag: mag[0] || null,
          protons: protons[0] || null,
          xray: xray[0] || null,
        })
      ),
    },
  };
};

export default function Home({ latestData }: { latestData: any }) {
  const stats = [
    {
      name: "Planetary Kp Index",
      value: latestData.kp?.kpIndex ?? "N/A",
      description: "Latest global geomagnetic activity",
      icon: Activity,
      color: "text-blue-600",
    },
    {
      name: "Magnetic Field (Bt)",
      value: latestData.mag?.bt ? `${latestData.mag.bt.toFixed(2)} nT` : "N/A",
      description: "Total interplanetary magnetic field",
      icon: Magnet,
      color: "text-indigo-600",
    },
    {
      name: "Proton Flux",
      value: latestData.protons?.flux ? `${latestData.protons.flux.toFixed(2)} pfu` : "N/A",
      description: "Latest integral proton flux",
      icon: Zap,
      color: "text-yellow-600",
    },
    {
      name: "X-Ray Flux",
      value: latestData.xray?.flux ? latestData.xray.flux.toExponential(2) : "N/A",
      description: "Latest solar X-ray radiation",
      icon: Sun,
      color: "text-orange-600",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Space Weather Overview</h2>
        <p className="text-muted-foreground">Latest observations from global monitoring systems.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{stat.name}</CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground">{stat.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Welcome to the Dashboard</CardTitle>
            <CardDescription>
              This dashboard provides real-time analysis of space weather conditions using data from DSCOVR, GOES, and planetary observatories.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm">
              Use the sidebar to navigate through detailed analysis sections, including:
            </p>
            <ul className="list-disc list-inside text-sm space-y-1 text-muted-foreground">
              <li><strong>Geomagnetism:</strong> Global and local K-index markers for geomagnetic storms.</li>
              <li><strong>Magnetic Field:</strong> DSCOVR magnetometer data at Lagrange point L1.</li>
              <li><strong>Proton Radiation:</strong> Charged particle fluxes from the Sun and deep space.</li>
              <li><strong>Solar X-Ray:</strong> Solar flare monitoring and classification.</li>
              <li><strong>Solar Regions:</strong> Evolution and statistics of active sunspot regions.</li>
            </ul>
          </CardContent>
        </Card>
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>System Information</CardTitle>
            <CardDescription>Data Sources and Availability</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center">
                <div className="h-2 w-2 rounded-full bg-green-500 mr-2" />
                <span className="text-sm font-medium">Database Connection: Online</span>
              </div>
              <div className="flex items-center">
                <div className="h-2 w-2 rounded-full bg-green-500 mr-2" />
                <span className="text-sm font-medium">Data Fetching: Active</span>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">
              Data is automatically synchronized from NOAA SWPC resources every few minutes.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
