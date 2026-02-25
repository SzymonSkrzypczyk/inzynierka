import { db } from "../db";
import { planetaryKIndex, dscovrMag, primaryIntegralProtons, primaryXray, solarRegions } from "../db/schema";
import { desc, sql, eq, and, lte } from "drizzle-orm";

export async function getPlanetaryKIndex(limit: number = 100) {
    return await db.query.planetaryKIndex.findMany({
        orderBy: [desc(planetaryKIndex.timeTag)],
        limit: limit,
    });
}

export async function getDscovrMag(limit: number = 100) {
    return await db.query.dscovrMag.findMany({
        orderBy: [desc(dscovrMag.timeTag)],
        limit: limit,
    });
}

export async function getPrimaryProtons(limit: number = 100) {
    return await db.query.primaryIntegralProtons.findMany({
        orderBy: [desc(primaryIntegralProtons.timeTag)],
        limit: limit,
    });
}

export async function getPrimaryXray(limit: number = 100) {
    return await db.query.primaryXray.findMany({
        orderBy: [desc(primaryXray.timeTag)],
        limit: limit,
    });
}

export async function getSolarRegions(limit: number = 100) {
    return await db.query.solarRegions.findMany({
        orderBy: [desc(solarRegions.observedDate)],
        limit: limit,
    });
}
