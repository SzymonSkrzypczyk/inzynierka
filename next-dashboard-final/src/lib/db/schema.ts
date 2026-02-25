import { pgTable, bigint, timestamp, smallint, real, varchar, date } from "drizzle-orm/pg-core";

export const planetaryKIndex = pgTable("planetary_k_index1ms", {
    id: bigint("id", { mode: "number" }).primaryKey(),
    timeTag: timestamp("time_tag"),
    kpIndex: smallint("kp_index"),
    estimatedKp: real("estimated_kp"),
    kp: varchar("kp", { length: 255 }),
});

export const dscovrMag = pgTable("dscovr_mag1s", {
    id: bigint("id", { mode: "number" }).primaryKey(),
    timeTag: timestamp("time_tag"),
    bt: real("bt"),
    bxGsm: real("bx_gsm"),
    byGsm: real("by_gsm"),
    bzGsm: real("bz_gsm"),
});

export const primaryIntegralProtons = pgTable("primary_integral_protons1_days", {
    id: bigint("id", { mode: "number" }).primaryKey(),
    timeTag: timestamp("time_tag"),
    satellite: smallint("satellite"),
    flux: real("flux"),
    energy: varchar("energy", { length: 255 }),
});

export const primaryXray = pgTable("primary_xray1_days", {
    id: bigint("id", { mode: "number" }).primaryKey(),
    timeTag: timestamp("time_tag"),
    satellite: smallint("satellite"),
    flux: real("flux"),
});

export const solarRegions = pgTable("solar_regions", {
    id: bigint("id", { mode: "number" }).primaryKey(),
    observedDate: date("observed_date"),
    region: smallint("region"),
    area: smallint("area"),
    magClass: varchar("mag_class", { length: 255 }),
    mXrayEvents: smallint("m_xray_events"),
    xXrayEvents: smallint("x_xray_events"),
    mFlareProbability: smallint("m_flare_probability"),
    xFlareProbability: smallint("x_flare_probability"),
});
