#!/usr/bin/env python3
"""
Generate apps/Samsara/samsara_trips_report_v2.json
Proper Retool Transit JSON format based on real app structure.
"""

import json
import uuid
import os

# ─── Load hotel-search app for Transit JSON header/tail ───────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOTEL_APP = os.path.join(BASE_DIR, 'apps', 'hotel-search-app-2026-01-30_164110.json')
OUTPUT    = os.path.join(BASE_DIR, 'apps', 'Samsara', 'samsara_trips_report_v2.json')

with open(HOTEL_APP) as f:
    hotel_data = json.load(f)

hotel_app_state = hotel_data['page']['data']['appState']

# Extract header: everything up to (and including) the opening '[' of the plugins list
plugins_key_idx   = hotel_app_state.find('"plugins"')
plugins_om_idx    = hotel_app_state.find('["~#iOM"', plugins_key_idx)
plugins_list_open = hotel_app_state.find('[', plugins_om_idx + 8)
HEADER = hotel_app_state[:plugins_list_open + 1]

# Extract tail: everything after the last plugin's ^1L footer
last_footer_idx = hotel_app_state.rfind('"^1L",null]]]')
TAIL = hotel_app_state[last_footer_idx + len('"^1L",null]]]'):]
# TAIL looks like: ']],"preloadedAppJavaScript",null,...]]]]'

# ─── Constants ────────────────────────────────────────────────────────────────
APP_UUID   = str(uuid.uuid4())
PAGE1_UUID = str(uuid.uuid4())
TS         = '~m1769620000000'   # fixed timestamp (arbitrary past date)

# ─── Helper ───────────────────────────────────────────────────────────────────
def je(s):
    """JSON-encode a string and strip outer quotes (for embedding in Transit JSON)."""
    return json.dumps(s, ensure_ascii=False)[1:-1]


# ─── Transformer JavaScript ───────────────────────────────────────────────────
TRANSFORMER_JS = (
    "// ─── CONFIG — change this to match your fleet's timezone ───────────────────\n"
    "const FLEET_TIMEZONE = 'America/New_York';\n"
    "// ───────────────────────────────────────────────────────────────────────────\n\n"
    "function formatDuration(totalSeconds) {\n"
    "  if (totalSeconds == null) return '--';\n"
    "  const h = Math.floor(totalSeconds / 3600);\n"
    "  const m = Math.floor((totalSeconds % 3600) / 60);\n"
    "  const s = totalSeconds % 60;\n"
    "  if (h > 0) return `${h}h ${String(m).padStart(2,'0')}m`;\n"
    "  return `${String(m).padStart(2,'0')}m ${String(s).padStart(2,'0')}s`;\n"
    "}\n\n"
    "function haversineMeters(lat1, lon1, lat2, lon2) {\n"
    "  const R = 6371000;\n"
    "  const toRad = d => d * Math.PI / 180;\n"
    "  const dLat = toRad(lat2 - lat1), dLon = toRad(lon2 - lon1);\n"
    "  const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon/2)**2;\n"
    "  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));\n"
    "}\n\n"
    "function findMatchingAddress(lat, lon, addressRaw, savedAddresses) {\n"
    "  for (const addr of savedAddresses) {\n"
    "    if (addr.latitude && addr.longitude) {\n"
    "      const dist = haversineMeters(lat, lon, addr.latitude, addr.longitude);\n"
    "      if (dist <= (addr.radius_meters || 200)) return addr;\n"
    "    }\n"
    "  }\n"
    "  const raw = (addressRaw || '').toLowerCase().trim();\n"
    "  return savedAddresses.find(a => (a.formatted_address || '').toLowerCase().trim() === raw) || null;\n"
    "}\n\n"
    "function toLocalDateString(epochMs) {\n"
    "  return new Date(epochMs).toLocaleDateString('en-US', {\n"
    "    timeZone: FLEET_TIMEZONE, year: 'numeric', month: '2-digit', day: '2-digit'\n"
    "  });\n"
    "}\n\n"
    "function toLocalTimeString(epochMs) {\n"
    "  return new Date(epochMs).toLocaleTimeString('en-US', {\n"
    "    timeZone: FLEET_TIMEZONE, hour: 'numeric', minute: '2-digit', hour12: true\n"
    "  });\n"
    "}\n\n"
    "// ─── Normalize Samsara API responses ───────────────────────────────────────\n"
    "const rawTrips    = (qGetTrips.data && qGetTrips.data.trips) ? qGetTrips.data.trips : [];\n"
    "const rawIdling   = (qGetIdlingEvents.data && qGetIdlingEvents.data.data) ? qGetIdlingEvents.data.data : [];\n"
    "const rawAddresses= (qGetAddresses.data && qGetAddresses.data.data) ? qGetAddresses.data.data : [];\n\n"
    "if (rawTrips.length === 0) return [];\n\n"
    "const trips = rawTrips.map(t => ({\n"
    "  id:                t.id,\n"
    "  start_time_ms:     t.startMs,\n"
    "  end_time_ms:       t.endMs,\n"
    "  distance_meters:   t.distanceMeters || 0,\n"
    "  start_address_raw: t.startAddress || '',\n"
    "  end_address_raw:   t.endAddress || '',\n"
    "  start_lat:         t.startCoordinates ? t.startCoordinates.latitude  : null,\n"
    "  start_lng:         t.startCoordinates ? t.startCoordinates.longitude : null,\n"
    "  end_lat:           t.endCoordinates   ? t.endCoordinates.latitude    : null,\n"
    "  end_lng:           t.endCoordinates   ? t.endCoordinates.longitude   : null,\n"
    "  driver_id:         t.driverId || null,\n"
    "}));\n\n"
    "const idling = rawIdling.map(e => ({\n"
    "  start_time_ms:    new Date(e.startTime).getTime(),\n"
    "  end_time_ms:      new Date(e.endTime || e.startTime).getTime(),\n"
    "  duration_seconds: e.durationMs ? Math.floor(e.durationMs / 1000) : 0,\n"
    "}));\n\n"
    "const addresses = rawAddresses.map(a => ({\n"
    "  id:                a.id,\n"
    "  name:              a.name,\n"
    "  formatted_address: a.formattedAddress || '',\n"
    "  latitude:          a.latitude  || null,\n"
    "  longitude:         a.longitude || null,\n"
    "  radius_meters:     (a.geofence && a.geofence.circle) ? a.geofence.circle.radius : 200,\n"
    "}));\n\n"
    "function getIdleForTrip(trip) {\n"
    "  return idling\n"
    "    .filter(e => e.start_time_ms >= trip.start_time_ms && e.start_time_ms <= trip.end_time_ms)\n"
    "    .reduce((sum, e) => sum + e.duration_seconds, 0);\n"
    "}\n\n"
    "const sorted = trips.slice().sort((a, b) => a.start_time_ms - b.start_time_ms);\n\n"
    "const byDate = {};\n"
    "for (const trip of sorted) {\n"
    "  const d = toLocalDateString(trip.start_time_ms);\n"
    "  if (!byDate[d]) byDate[d] = [];\n"
    "  byDate[d].push(trip);\n"
    "}\n\n"
    "const rows = [];\n\n"
    "for (const dateStr of Object.keys(byDate).sort()) {\n"
    "  const dayTrips = byDate[dateStr];\n"
    "  let dayMiles = 0, dayDriveSecs = 0, dayIdleSecs = 0, dayStopSecs = 0;\n\n"
    "  const first = dayTrips[0];\n"
    "  const startMatch = findMatchingAddress(first.start_lat, first.start_lng, first.start_address_raw, addresses);\n"
    "  rows.push({\n"
    "    row_type:           'start_header',\n"
    "    trip_date:          dateStr,\n"
    "    stop_location_raw:  first.start_address_raw,\n"
    "    stop_is_geofence:   !!startMatch,\n"
    "    stop_geofence_name: startMatch ? startMatch.name : null,\n"
    "  });\n\n"
    "  for (let i = 0; i < dayTrips.length; i++) {\n"
    "    const trip = dayTrips[i];\n"
    "    const next = dayTrips[i + 1] || null;\n"
    "    const driveSecs  = Math.round((trip.end_time_ms - trip.start_time_ms) / 1000);\n"
    "    const distMiles  = parseFloat((trip.distance_meters / 1609.344).toFixed(2));\n"
    "    const idleSecs   = getIdleForTrip(trip);\n"
    "    const stopSecs   = next ? Math.max(0, Math.round((next.start_time_ms - trip.end_time_ms) / 1000)) : null;\n"
    "    const endMatch   = findMatchingAddress(trip.end_lat, trip.end_lng, trip.end_address_raw, addresses);\n"
    "    dayMiles     += distMiles;\n"
    "    dayDriveSecs += driveSecs;\n"
    "    dayIdleSecs  += idleSecs;\n"
    "    if (stopSecs != null) dayStopSecs += stopSecs;\n"
    "    rows.push({\n"
    "      row_type:               'trip',\n"
    "      trip_date:              dateStr,\n"
    "      trip_id:                trip.id,\n"
    "      start_time_display:     toLocalTimeString(trip.start_time_ms),\n"
    "      distance_miles:         distMiles,\n"
    "      drive_duration_display: formatDuration(driveSecs),\n"
    "      stop_location_raw:      trip.end_address_raw,\n"
    "      stop_is_geofence:       !!endMatch,\n"
    "      stop_geofence_name:     endMatch ? endMatch.name : null,\n"
    "      arrival_time_display:   toLocalTimeString(trip.end_time_ms),\n"
    "      idle_duration_display:  formatDuration(idleSecs),\n"
    "      stop_duration_display:  stopSecs != null ? formatDuration(stopSecs) : '--',\n"
    "    });\n"
    "  }\n\n"
    "  rows.push({\n"
    "    row_type:              'total',\n"
    "    trip_date:             dateStr,\n"
    "    stop_count:            dayTrips.length,\n"
    "    distance_miles:        parseFloat(dayMiles.toFixed(2)),\n"
    "    idle_duration_display: formatDuration(dayIdleSecs),\n"
    "    stop_duration_display: formatDuration(dayStopSecs),\n"
    "    totals_label:          parseFloat(dayMiles.toFixed(2)) + ' miles in ' + formatDuration(dayDriveSecs),\n"
    "  });\n"
    "}\n\n"
    "return rows;"
)

# ─── Column definitions ────────────────────────────────────────────────────────
COL_IDS = ['aa001', 'bb002', 'cc003', 'dd004', 'ee005', 'ff006']

COL_KEY = {
    'aa001': 'start_time_display',
    'bb002': 'distance_miles',
    'cc003': 'stop_location_raw',
    'dd004': 'arrival_time_display',
    'ee005': 'idle_duration_display',
    'ff006': 'stop_duration_display',
}

COL_TITLE = {
    'aa001': 'START TIME',
    'bb002': 'DIST / DURATION',
    'cc003': 'STOP LOCATION',
    'dd004': 'ARRIVAL TIME',
    'ee005': 'IDLE DURATION',
    'ff006': 'STOP DURATION',
}

COL_FORMAT = {
    'aa001': 'string',
    'bb002': 'string',
    'cc003': 'html',
    'dd004': 'string',
    'ee005': 'string',
    'ff006': 'string',
}

COL_ALIGNMENT = {
    'aa001': 'left',
    'bb002': 'left',
    'cc003': 'left',
    'dd004': 'left',
    'ee005': 'right',
    'ff006': 'right',
}

# Retool column value expressions (these will be JSON-escaped via je())
_start_time_expr = "{{ currentSourceRow.row_type !== 'total' && currentSourceRow.row_type !== 'start_header' ? currentSourceRow.start_time_display : '' }}"
_dist_dur_expr   = "{{ currentSourceRow.row_type === 'total' ? currentSourceRow.totals_label : (currentSourceRow.row_type === 'start_header' ? '' : currentSourceRow.distance_miles + ' mi  \u2022  ' + currentSourceRow.drive_duration_display) }}"
_stop_loc_expr   = ("{{ (function() {"
                    " var row = currentSourceRow;"
                    " if (row.row_type === 'start_header') {"
                    "   return '<span style=\"font-style:italic\">Starting from:</span> ' +"
                    "          (row.stop_is_geofence"
                    "             ? '<span style=\"color:red\">[' + row.stop_location_raw + ']</span><br/>' + row.stop_location_raw"
                    "             : (row.stop_location_raw || ''));"
                    " }"
                    " if (row.row_type === 'total') {"
                    "   return '<strong>Total \u2014 ' + row.stop_count + ' stops</strong>';"
                    " }"
                    " if (row.stop_is_geofence) {"
                    "   return '<span style=\"color:red\">[' + row.stop_location_raw + ']</span><br/>' + row.stop_location_raw;"
                    " }"
                    " return row.stop_location_raw || '';"
                    " })() }}")
_arrival_expr    = "{{ currentSourceRow.row_type === 'trip' ? currentSourceRow.arrival_time_display : '' }}"
_idle_expr       = "{{ currentSourceRow.idle_duration_display || '' }}"
_stop_dur_expr   = "{{ currentSourceRow.stop_duration_display || '' }}"

COL_VALUE_OVERRIDE = {
    'aa001': _start_time_expr,
    'bb002': _dist_dur_expr,
    'cc003': _stop_loc_expr,
    'dd004': _arrival_expr,
    'ee005': _idle_expr,
    'ff006': _stop_dur_expr,
}

_dist_color_expr = "{{ currentSourceRow.row_type === 'trip' ? '#e6820e' : 'inherit' }}"

COL_TEXT_COLOR = {
    'aa001': '',
    'bb002': _dist_color_expr,
    'cc003': '',
    'dd004': '',
    'ee005': '',
    'ff006': '',
}

_row_color_expr = "{{ currentSourceRow.row_type === 'total' ? '#f0f0f0' : currentSourceRow.row_type === 'start_header' ? '#f9f9f9' : '#ffffff' }}"


# ─── Column map builders ───────────────────────────────────────────────────────
def cmap(d, val_fn=None):
    """Build a Transit ["^1M",[...]] map from a dict keyed by column ID."""
    parts = []
    for cid in COL_IDS:
        raw = d.get(cid, '')
        val = val_fn(raw) if val_fn else f'"{raw}"'
        parts.append(f'"{cid}",{val}')
    return '["^1M",[' + ','.join(parts) + ']]'

def cmap_str(d):    return cmap(d)
def cmap_expr(d):   return cmap(d, lambda v: f'"{je(v)}"')
def cmap_bool(val): return '["^1M",[' + ','.join(f'"{c}",{str(val).lower()}' for c in COL_IDS) + ']]'
def cmap_obj(val):  return '["^1M",[' + ','.join(f'"{c}",{val}' for c in COL_IDS) + ']]'

col_ids_str             = '["^A",[' + ','.join(f'"{c}"' for c in COL_IDS) + ']]'
col_empty_str           = cmap_str({c: '' for c in COL_IDS})
col_key_map             = cmap_str(COL_KEY)
col_title_map           = cmap_str(COL_TITLE)
col_format_map          = cmap_str(COL_FORMAT)
col_alignment_map       = cmap_str(COL_ALIGNMENT)
col_value_override_map  = cmap_expr(COL_VALUE_OVERRIDE)
col_text_color_map      = cmap_expr(COL_TEXT_COLOR)
col_sort_disabled_map   = cmap_bool(False)
col_search_mode_map     = cmap_str({c: 'default' for c in COL_IDS})
col_editable_opts_map   = cmap_obj('["^1M",[]]')
col_cell_tooltip_map    = cmap_str({c: '' for c in COL_IDS})
col_tooltip_map         = cmap_str({c: '' for c in COL_IDS})
col_icon_map            = cmap_str({c: '' for c in COL_IDS})


# ─── Footer builder ────────────────────────────────────────────────────────────
def footer(container='', screen='page1'):
    return (
        f'"^1A",["^1M",[]],'
        f'"^1B",null,'
        f'"^1C",null,"^1D",null,"^1E",null,'
        f'"^1F","{container}",'
        f'"^7","{TS}","^1G","{TS}",'
        f'"^1H","","^1I",null,"^1J","{screen}","^1K",null,"^1L",null'
    )

def footer_with_pos(container, row, col, height, width, screen='page1'):
    pos2 = (
        f'["^0",["^ ","n","position2","v",'
        f'["^ ","^1;","grid","^1F","{container}","^1N","body","^1O","",'
        f'"row",{row},"col",{col},'
        f'"^1P",{height},"^1Q",{width},'
        f'"^1R",0,"^1S",null]]]'
    )
    return (
        f'"^1A",["^1M",[]],'
        f'"^1B",{pos2},'
        f'"^1C",null,"^1D",null,"^1E",null,'
        f'"^1F","{container}",'
        f'"^7","{TS}","^1G","{TS}",'
        f'"^1H","","^1I",null,"^1J","{screen}","^1K",null,"^1L",null'
    )


# ─── Plugin builders ───────────────────────────────────────────────────────────

def plugin_wrap(plugin_id, inner):
    """Wrap plugin content: "pluginId",["^0",["^ ","n","pluginTemplate","v",[...inner...,footer]]]"""
    return f'"{plugin_id}",["^0",["^ ","n","pluginTemplate","v",["^ ",{inner}]]]'


# 1. page1 Screen  (first plugin — uses full key names because cache is fresh)
def make_page1():
    return (
        f'"page1",["^0",["^ ",'
        f'"n","pluginTemplate","v",["^ ",'
        f'"id","page1",'
        f'"uuid","{PAGE1_UUID}",'
        f'"_comment",null,'
        f'"type","screen",'
        f'"subtype","Screen",'
        f'"namespace",null,'
        f'"resourceName",null,'
        f'"resourceDisplayName",null,'
        f'"template",["^18",["title","Samsara Trips Report","browserTitle","","urlSlug","","_order",0,"_searchParams",["^A",[]],"_hashParams",["^A",[]],"_customShortcuts",["^A",[]]]],'
        f'"style",null,'
        f'"position2",null,'
        f'"mobilePosition2",null,'
        f'"mobileAppPosition",null,'
        f'"tabIndex",null,'
        f'"container","",'
        f'"^7","{TS}",'
        f'"updatedAt","{TS}",'
        f'"folder","",'
        f'"presetName",null,'
        f'"screen",null,'
        f'"boxId",null,'
        f'"subBoxIds",null'
        f']]]'
    )


# 2. $main Frame  (second plugin — uses cached keys ^1; etc.)
def make_main_frame():
    inner = (
        f'"id","$main","^19",null,"^1:",null,'
        f'"^1;","frame","^1<","Frame","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["~#iM",["type","main","padding","8px 12px","enableFullBleed",false,"isHiddenOnDesktop",false,"isHiddenOnMobile",false]],'
        + footer(container='', screen='page1')
    )
    return plugin_wrap('$main', inner)


# 3. vehicleSelect — SelectWidget2 (dynamic options from qGetVehicles)
def make_vehicle_select():
    inner = (
        f'"id","vehicleSelect","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","SelectWidget2","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"readOnly",false,"iconAfter","","hidden",false,"customValidation","",'
        f'"hideValidationMessage",false,"textBefore","","validationMessage","",'
        f'"margin","4px 8px","textAfter","","showInEditor",false,"showClear",true,'
        f'"tooltipText","","labelAlign","left","formDataKey","{{{{ self.id }}}}",'
        f'"values","{{{{ (qGetVehicles.data.data || []).map(v => v.id) }}}}",'
        f'"labels","{{{{ (qGetVehicles.data.data || []).map(v => v.name) }}}}",'
        f'"value",null,"labelCaption","","labelWidth","33",'
        f'"label","Vehicle","placeholder","Select a vehicle...",'
        f'"labelWidthUnit","%","labelPosition","top","invalid",false,'
        f'"events",["^18",[]],"loading",false,"disabled",false,'
        f'"required",false,"maintainSpaceWhenHidden",false'
        f']],'
        + footer_with_pos('$main', 0, 0, 8, 4)
    )
    return plugin_wrap('vehicleSelect', inner)


# 4. dateStart — DateWidget (start date)
def make_date_start():
    inner = (
        f'"id","dateStart","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","DateWidget","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"minDate","","readOnly",false,"iconAfter","",'
        f'"datePlaceholder","{{{{ self.dateFormat.toUpperCase() }}}}",'
        f'"dateFormat","MM/DD/YYYY","hidden",false,"customValidation","",'
        f'"hideValidationMessage",false,"textBefore","","validationMessage","",'
        f'"margin","4px 8px","textAfter","","showInEditor",false,"showClear",false,'
        f'"tooltipText","","labelAlign","left","formDataKey","{{{{ self.id }}}}",'
        f'"value","{{{{ new Date(Date.now() - 7*24*3600*1000) }}}}",'
        f'"labelCaption","","maxDate","","labelWidth","33",'
        f'"label","From Date","formattedValue","","_validate",false,'
        f'"labelWidthUnit","%","firstDayOfWeek",0,"invalid",false,'
        f'"iconBefore","bold/interface-calendar","events",["^18",[]],'
        f'"loading",false,"disabled",false,"labelPosition","top",'
        f'"labelWrap",false,"maintainSpaceWhenHidden",false,"required",false'
        f']],'
        + footer_with_pos('$main', 0, 4, 8, 4)
    )
    return plugin_wrap('dateStart', inner)


# 5. dateEnd — DateWidget (end date)
def make_date_end():
    inner = (
        f'"id","dateEnd","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","DateWidget","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"minDate","","readOnly",false,"iconAfter","",'
        f'"datePlaceholder","{{{{ self.dateFormat.toUpperCase() }}}}",'
        f'"dateFormat","MM/DD/YYYY","hidden",false,"customValidation","",'
        f'"hideValidationMessage",false,"textBefore","","validationMessage","",'
        f'"margin","4px 8px","textAfter","","showInEditor",false,"showClear",false,'
        f'"tooltipText","","labelAlign","left","formDataKey","{{{{ self.id }}}}",'
        f'"value","{{{{ new Date() }}}}",'
        f'"labelCaption","","maxDate","","labelWidth","33",'
        f'"label","To Date","formattedValue","","_validate",false,'
        f'"labelWidthUnit","%","firstDayOfWeek",0,"invalid",false,'
        f'"iconBefore","bold/interface-calendar","events",["^18",[]],'
        f'"loading",false,"disabled",false,"labelPosition","top",'
        f'"labelWrap",false,"maintainSpaceWhenHidden",false,"required",false'
        f']],'
        + footer_with_pos('$main', 0, 8, 8, 4)
    )
    return plugin_wrap('dateEnd', inner)


# 6. btnRun — ButtonWidget2
def make_btn_run():
    # Event: onClick triggers qGetTrips and qGetIdlingEvents
    on_click = je("qGetTrips.trigger(); qGetIdlingEvents.trigger();")
    inner = (
        f'"id","btnRun","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","ButtonWidget2","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"heightType","fixed","horizontalAlign","stretch","clickable",false,'
        f'"iconAfter","","submitTargetId",null,"hidden",false,"ariaLabel","",'
        f'"text","Run Report","margin","4px 8px","showInEditor",false,'
        f'"tooltipText","","allowWrap",true,"styleVariant","solid","submit",false,'
        f'"iconBefore","",'
        f'"events",["^A",[["^1M",["method","run","params",["^1M",["src","{on_click}"]],'
        f'"targetId",null,"pluginId","","waitType","debounce","event","click",'
        f'"type","script","id","run001","waitMs","0"]]]],'
        f'"loading",false,"loaderPosition","auto","disabled",false,"maintainSpaceWhenHidden",false'
        f']],'
        + footer_with_pos('$main', 10, 0, 5, 2)
    )
    return plugin_wrap('btnRun', inner)


# 7. txtHeader — TextWidget2
def make_txt_header():
    header_text = je("#### {{ (qGetVehicles.data.data || []).find(v => v.id === vehicleSelect.value)?.name || 'Select a vehicle to run report' }}")
    inner = (
        f'"id","txtHeader","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","TextWidget2","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"heightType","auto","horizontalAlign","left","hidden",false,'
        f'"imageWidth","fit","margin","4px 8px","showInEditor",false,'
        f'"verticalAlign","center","tooltipText","","value","{header_text}",'
        f'"disableMarkdown",false,"overflowType","scroll","maintainSpaceWhenHidden",false'
        f']],'
        + footer_with_pos('$main', 16, 0, 5, 12)
    )
    return plugin_wrap('txtHeader', inner)


# 8. tblReport — TableWidget2
def make_tbl_report():
    row_color = je(_row_color_expr)
    inner = (
        f'"id","tblReport","^19",null,"^1:",null,'
        f'"^1;","widget","^1<","TableWidget2","^1=",null,"^1>",null,"^1?",null,'
        f'"^1@",["^1M",['
        f'"selectedRowKey",null,"_nextAfterCursor","","_columnBackgroundColor",{col_empty_str},'
        f'"_defaultSort",null,"_columnSearchMode",{col_search_mode_map},'
        f'"_columnAlternateRowBackgroundColor",{col_empty_str},'
        f'"_clearChangesetOnSave",true,"heightType","fixed",'
        f'"_columnTextColor",{col_text_color_map},'
        f'"disableEdits",true,"autoColumnWidth",false,"_rowHeight","medium",'
        f'"_columnIds",{col_ids_str},'
        f'"_isSaving",false,"_headerTextWrap",false,"_actionIds",["^A",[]],'
        f'"_clearChangeset",false,"caseSensitiveFiltering",false,'
        f'"_limitOffsetRowCount",null,"selectedSourceRow",null,'
        f'"_dynamicColumnsEnabled",false,"disableSave",true,'
        f'"_columnEditableOptions",{col_editable_opts_map},'
        f'"_toolbarPosition","bottom","_groupByColumns",["^A",[]],'
        f'"_nextBeforeCursor","","_persistRowSelection",false,'
        f'"_showBorder",true,"_templatePageSize",null,'
        f'"_dynamicColumnProperties",["^1M",[]],'
        f'"_showHeader",true,"_currentPage",0,'
        f'"overflowActionsOverlayMinWidth",null,"_actionsOverflowPosition",0,'
        f'"_columnKey",{col_key_map},'
        f'"hidden",false,"columnOrdering",[],'
        f'"data","{{{{ transformReportData.data }}}}",'
        f'"_cellSelection","none","_serverPaginated",false,'
        f'"_linkedFilterId",null,"searchMode","fuzzy",'
        f'"_columnFormat",{col_format_map},'
        f'"_primaryKeyColumnId","aa001","selectedDataIndex",null,'
        f'"_columnAlignment",{col_alignment_map},'
        f'"_columnCellTooltip",{col_cell_tooltip_map},'
        f'"_columnTooltip",{col_tooltip_map},'
        f'"_columnIcon",{col_icon_map},'
        f'"margin","4px 8px","showInEditor",false,'
        f'"showPagination",true,"showSearch",false,'
        f'"showFilter",false,"showDownload",true,"showRefresh",true,'
        f'"_columnSortDisabled",{col_sort_disabled_map},'
        f'"_showSummaryRow",false,'
        f'"events",["^18",[]],"loading",false,'
        f'"_columnValueOverride",{col_value_override_map},'
        f'"_columnTitle",{col_title_map},'
        f'"_rowColor","{row_color}",'
        f'"style",["^1M",["rowSeparator","surfacePrimaryBorder"]]'
        f']],'
        + footer_with_pos('$main', 22, 0, 54, 12)
    )
    return plugin_wrap('tblReport', inner)


# ─── Query plugin builder ──────────────────────────────────────────────────────

def make_rest_query(qid, path, run_on_load=False, success_events='["^A",[]]'):
    """Build a RESTQuery plugin targeting the 'Samsara' resource."""
    query_str = je(path)
    trigger_val = 'true' if run_on_load else 'false'
    inner = (
        f'"id","{qid}","^19",null,"^1:",null,'
        f'"^1;","datasource","^1<","RESTQuery","^1=",null,'
        f'"^1>","Samsara","^1?","Samsara",'
        f'"^1@",["^1M",['
        f'"queryRefreshTime","","paginationLimit","","allowedGroupIds",["^A",[]],'
        f'"streamResponse",false,"body","","lastReceivedFromResourceAt",null,'
        f'"isFunction",false,"functionParameters",null,"queryDisabledMessage","",'
        f'"servedFromCache",false,"offlineUserQueryInputs","","functionDescription",null,'
        f'"successMessage","","queryDisabled","","playgroundQuerySaveId","latest",'
        f'"workflowParams",null,"resourceNameOverride","","runWhenModelUpdates",false,'
        f'"paginationPaginationField","","bodyRaw",null,"workflowRunExecutionType","sync",'
        f'"headers","","showFailureToaster",true,"paginationEnabled",false,'
        f'"query","{query_str}",'
        f'"playgroundQueryUuid","","playgroundQueryId",null,"error",null,'
        f'"workflowRunBodyType","raw","privateParams",["^A",[]],'
        f'"queryRunOnSelectorUpdate",false,"runWhenPageLoadsDelay","","data",null,'
        f'"importedQueryInputs",["^1M",[]],"isImported",false,'
        f'"showSuccessToaster",false,"cacheKeyTtl","","requestSentTimestamp",null,'
        f'"cookies","","metadata",null,"queryRunTime",null,"bodyFormData",null,'
        f'"changesetObject","","offlineOptimisticResponse",null,'
        f'"errorTransformer","return data.error","finished",null,'
        f'"confirmationMessage",null,"isFetching",false,"changeset","","rawData",null,'
        f'"queryTriggerDelay","0","resourceTypeOverride",null,'
        f'"watchedParams",["^A",[]],"enableErrorTransformer",false,'
        f'"showLatestVersionUpdatedWarning",false,"paginationDataField","","timestamp",0,'
        f'"openAPIParams","{{}}","importedQueryDefaults",["^1M",[]],'
        f'"enableTransformer",false,"showUpdateSetValueDynamicallyToggle",true,'
        f'"version",2,"overrideOrgCacheForUserCache",false,'
        f'"runWhenPageLoads",{trigger_val},"transformer","return data",'
        f'"events",{success_events},'
        f'"queryTimeout","10000","workflowId",null,'
        f'"requireConfirmation",false,"type","GET",'
        f'"queryFailureConditions","","changesetIsObject",false,'
        f'"enableCaching",false,"allowedGroups",["^A",[]],'
        f'"bodyType","none","offlineQueryType","None",'
        f'"queryThrottleTime","750","updateSetValueDynamically",false,'
        f'"notificationDuration",""'
        f']],'
        + footer(screen='page1')
    )
    return plugin_wrap(qid, inner)


def make_js_query(qid, code, run_on_load=False):
    """Build a JavascriptQuery plugin."""
    code_escaped = je(code)
    trigger_val = 'true' if run_on_load else 'false'
    inner = (
        f'"id","{qid}","^19",null,"^1:",null,'
        f'"^1;","datasource","^1<","JavascriptQuery","^1=",null,'
        f'"^1>","JavascriptQuery","^1?",null,'
        f'"^1@",["^1M",['
        f'"queryRefreshTime","","allowedGroupIds",["^A",[]],'
        f'"streamResponse",false,"lastReceivedFromResourceAt",null,'
        f'"isFunction",false,"functionParameters",null,"queryDisabledMessage","",'
        f'"servedFromCache",false,"offlineUserQueryInputs","","functionDescription",null,'
        f'"successMessage","","queryDisabled","","playgroundQuerySaveId","latest",'
        f'"workflowParams",null,"resourceNameOverride","","runWhenModelUpdates",false,'
        f'"workflowRunExecutionType","sync","showFailureToaster",true,'
        f'"query","{code_escaped}",'
        f'"playgroundQueryUuid","","playgroundQueryId",null,"error",null,'
        f'"workflowRunBodyType","raw","privateParams",["^A",[]],'
        f'"queryRunOnSelectorUpdate",false,"runWhenPageLoadsDelay","","data",null,'
        f'"importedQueryInputs",["^1M",[]],"isImported",false,'
        f'"showSuccessToaster",false,"cacheKeyTtl","","requestSentTimestamp",null,'
        f'"metadata",null,"queryRunTime",null,'
        f'"offlineOptimisticResponse",null,'
        f'"errorTransformer","return data.error","finished",null,'
        f'"confirmationMessage",null,"isFetching",false,"rawData",null,'
        f'"queryTriggerDelay","0",'
        f'"watchedParams",["^A",[]],"enableErrorTransformer",false,'
        f'"showLatestVersionUpdatedWarning",false,"timestamp",0,'
        f'"importedQueryDefaults",["^1M",[]],"enableTransformer",false,'
        f'"showUpdateSetValueDynamicallyToggle",false,'
        f'"version",2,"overrideOrgCacheForUserCache",false,'
        f'"runWhenPageLoads",{trigger_val},'
        f'"events",["^18",[]],'
        f'"queryTimeout","10000","workflowId",null,'
        f'"requireConfirmation",false,'
        f'"queryFailureConditions","","changesetIsObject",false,'
        f'"allowedGroups",["^A",[]],'
        f'"offlineQueryType","None",'
        f'"queryThrottleTime","750","updateSetValueDynamically",false,'
        f'"notificationDuration",""'
        f']],'
        + footer(screen='page1')
    )
    return plugin_wrap(qid, inner)


# ─── Build all plugins ─────────────────────────────────────────────────────────

# REST query paths (query params embedded in URL path)
PATH_VEHICLES = '/fleet/vehicles'
PATH_ADDRESSES = '/addresses'
PATH_TRIPS = (
    '/v1/fleet/trips'
    '?vehicleId={{ vehicleSelect.value }}'
    '&startMs={{ dateStart.value ? new Date(dateStart.value).getTime() : \'\' }}'
    '&endMs={{ dateEnd.value ? new Date(dateEnd.value).getTime() : \'\' }}'
)
PATH_IDLING = (
    '/fleet/idlingEvents'
    '?vehicleIds={{ vehicleSelect.value }}'
    '&startTime={{ dateStart.value ? new Date(dateStart.value).toISOString() : \'\' }}'
    '&endTime={{ dateEnd.value ? new Date(dateEnd.value).toISOString() : \'\' }}'
)

plugins = [
    make_page1(),
    make_main_frame(),
    make_vehicle_select(),
    make_date_start(),
    make_date_end(),
    make_btn_run(),
    make_txt_header(),
    make_tbl_report(),
    make_rest_query('qGetVehicles',    PATH_VEHICLES,  run_on_load=True),
    make_rest_query('qGetAddresses',   PATH_ADDRESSES, run_on_load=True),
    make_rest_query('qGetTrips',       PATH_TRIPS,     run_on_load=False),
    make_rest_query('qGetIdlingEvents',PATH_IDLING,    run_on_load=False),
    make_js_query('transformReportData', TRANSFORMER_JS, run_on_load=False),
]

# ─── Assemble appState ────────────────────────────────────────────────────────
plugins_str = ','.join(plugins)
app_state   = HEADER + plugins_str + TAIL

# ─── Validate appState is parseable JSON ─────────────────────────────────────
try:
    json.loads(app_state)
    print('✓ appState is valid JSON')
except json.JSONDecodeError as e:
    print(f'✗ appState JSON error: {e}')
    print(f'  Context: ...{app_state[max(0, e.pos-80):e.pos+80]}...')
    raise

# ─── Build outer file structure ───────────────────────────────────────────────
output_data = {
    'uuid': APP_UUID,
    'page': {
        'id': 485864460,
        'data': {
            'appState': app_state
        },
        'changesRecord': [],
        'changesRecordV2': [],
        'checksum': None,
        'multiplayerSessionId': str(uuid.uuid4()),
        'appTestingSaveId': None,
        'subflows': None,
        'isCopilotGenerated': False,
        'createdAt': '2025-01-01T00:00:00.000Z',
        'updatedAt': '2025-01-01T00:00:00.000Z',
        'pageId': 4900000,
        'userId': 123456,
    },
    'modules': {}
}

# ─── Write output ─────────────────────────────────────────────────────────────
with open(OUTPUT, 'w') as f:
    json.dump(output_data, f, separators=(',', ':'))

print(f'✓ Written to {OUTPUT}')
file_size = os.path.getsize(OUTPUT)
print(f'  File size: {file_size:,} bytes')

# ─── Final validation ─────────────────────────────────────────────────────────
with open(OUTPUT) as f:
    verify = json.load(f)

parsed_state = json.loads(verify['page']['data']['appState'])
print(f'✓ Final validation passed — appState root: {parsed_state[0]}')
