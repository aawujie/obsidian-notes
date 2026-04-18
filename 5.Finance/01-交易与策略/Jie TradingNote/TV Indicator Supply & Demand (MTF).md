---
notion-id: 28478d23-e296-802e-a9ad-df358e01da63
Last edited time: 2025-10-12T02:20:00
Tags: []
Verification: unverified
Owner:
  - 杰 吴
---
## 概念

> TradingView 指标名称：Supply and Demand (MTF) | Flux Charts

- **供应区**是过去价格快速下跌、卖方力量显著的区域，当价格再次回到这里时，预计会遇到阻力，是**潜在的卖出（或看跌）机会**。
- **需求区**是过去价格快速上涨、买方力量显著的区域，当价格再次回到这里时，预计会遇到支撑，是**潜在的买入（或看涨）机会**。

![[imgs/image 216.png]]

![[imgs/image 217.png]]

1. **供应区 (Supply Zones) ****- 通常是****红色或熊市颜色框**
    - **识别方式**: **当价格在短时间内出现多根强劲的看跌K线（****实体大小大于平均水平****）**（由变量 momentumSpan 和 momentumCount 定义），**这表明有大量卖家在某一价格区间入场**。指标会根据这些K线之前的某个高点和低点来定义供应区。
    - **代表意义**: **供应区代表了市场中存在大量潜在的卖盘**。**当价格再次回到这个区域时，预计会遇到卖家的抛售压力，从而可能导致价格下跌**。这通常被视为潜在的**做空机会**或**现有多头头寸的平仓点**。
2. **需求区 (Demand Zones)**** - 通常是****绿色或牛市颜色框**
    - **识别方式**: **与供应区相反，当价格在短时间内出现多根强劲的看涨K线，表明有大量买家在某一价格区间入场**。指标会根据这些K线之前的某个高点和低点来定义需求区。
    - **代表意义**: 需求区代表了市场中**存在大量潜在的买盘**。**当价格再次回到这个区域时，预计会遇到买家的买入支撑，从而可能导致价格上涨**。这通常被视为潜在的**做多机会**或**现有空头头寸的平仓点**。
3. **区域失效 (Zone Invalidation)**
    - **代表意义**: **当价格完全穿透一个供应区或需求区时，意味着该区域的买卖失衡已经被消耗殆尽，**或者说**买卖双方的力量已经逆转**。该区域就不再有效。
    - **视觉呈现**: 默认情况下，**失效的区域仍然会显示，但其颜色可能会稍微透明化**。区域的方框会从其起始时间延伸到breakTime（突破时间），而不是延伸到当前K线。
4. **合并区域 (Combined Zones)**
    - **代表意义**: 如果**多个供应区（或需求区）在时间和价格上相互重叠，指标会尝试将它们合并成一个更大的、更强的区域**。这表明**在更广的价格范围内，存在持续的买盘或卖盘压力**。
    - **视觉呈现**: 合并后的区域通常会以稍微不同的颜色透明度显示，并且其文本标签可能会显示合并的多个时间周期（**例如“1 Hour & 30 Min Supply”**），表示这个区域是**多时间周期共振形成的**。
5. **重新测试标签 (Retest Labels - "R")**
    - **识别方式**: **当价格回撤到未失效的供应区或需求区边缘附近，但并未完全穿透它时，就会标记一个重新测试。**
    - **代表意义**: **重新测试表明市场正在再次确认这个区域的有效性**。**在需求区重新测试并反弹，可以看作是买家再次入场的信号；在供应区重新测试并下跌，可以看作是卖家再次入场的信号**。这通常被视为**高概率的交易入场点**。
    - **视觉呈现**: 在发生重新测试的K线处，会绘制一个带有“R”字母的标签。需求区重新测试通常是向上的绿色标签，供应区重新测试是向下的红色标签。
6. **突破标签 (Break Labels - "B")**
    - **识别方式**: **当价格有效穿透一个供应区或需求区，导致该区域失效时，就会标记一个突破**。
    - **代表意义**: **突破意味着市场力量的转换**。**突破需求区可能预示着下跌趋势的开始或延续；突破供应区可能预示着上涨趋势的开始或延续**。这可以被视为**趋势改变**或**趋势延续的信号**。
    - **视觉呈现**: 在发生突破的K线处，会绘制一个带有“B”字母的标签，通常是蓝色。向上突破供应区是向上的蓝色标签，向下突破需求区是向下的蓝色标签。
7. **多时间周期 (Multi-Timeframe, MTF)**
    - **代表意义**: 指标能够同时显示不同时间周期（例如15分钟、30分钟、1小时）的供应和需求区域。
    - **重要性**: **更高时间周期的区域通常比低时间周期的区域更具影响力**。**当低时间周期的价格行为与高时间周期的区域重合时，信号的强度和可靠性会大大增加**。例如，在一个15分钟图上看到价格进入一个1小时的需求区，这通常比仅仅在一个15分钟的需求区内更具说服力。

## **典型的交易策略应用**

8. **在需求区买入，在供应区卖出（****反转策略****）**:
    - 当价格进入一个**需求区**并显示出拒绝下跌的K线形态（例如，锤子线、吞噬形态等），交易者可能会考虑**做多**，止损设在需求区下方，目标是下一个供应区或结构高点。
    - 当价格进入一个**供应区**并显示出拒绝上涨的K线形态（例如，射击之星、看跌吞噬等），交易者可能会考虑**做空**，止损设在供应区上方，目标是下一个需求区或结构低点。
    - **“R” 标签（重新测试）**在这里是**关键的入场信号，它确认了区域的有效性**。
9. **交易区域突破（****趋势延续或趋势反转策略****）**:
    - 当价格**突破并收盘在供应区之上**时，这可能预示着**上涨趋势的延续或熊市结构的转变，交易者可能会考虑追多。**
    - 当价格**突破并收盘在需求区之下**时，这可能预示着**下跌趋势的延续或牛市结构的转变，交易者可能会考虑追空。**
    - **“B”标签（突破）**在这里提供了突破的确认。
10. **结合多时间周期分析**:
    - 交易者会寻找**高时间周期**（例如日线、4小时）和**低时间周期**（例如15分钟、1小时）区域的**共振**。例如，如果15分钟图上的价格进入了一个1小时和4小时图上的共同需求区域，这会大大增加该需求区域的可靠性，提供更强的买入信号。
    - **多时间周期区域的结合（通过合并区域功能显示）更能反映市场深层次的供需平衡。**

## 代码

```javascript
// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © fluxchart

//@version=5
const bool DEBUG = false
const int maxBoxesCount = 500
const float overlapThresholdPercentage = 0.0
int maxDistanceToLastBar = 1250 // Affects Running Time
const int maxSDZones = 30
const int minZoneSize = 10
const int RETEST_COOLDOWN   = 5
const int minDistanceBetweenZones = 5
const float maxZoneSizeATR = 1.5

indicator(title = 'Supply & Demand (MTF) | Flux Charts', shorttitle = "Supply and Demand (MTF) | Flux Charts", overlay = true, max_boxes_count = maxBoxesCount, max_labels_count = maxBoxesCount, max_lines_count = maxBoxesCount, max_bars_back = 2000, dynamic_requests = true)

maxDistanceString   = input.string("Normal", "Max Distance To Last Bar", options = ["High", "Normal", "Low"],  group = "General Configuration", display = display.none)
sdEndMethod = input.string("Close", "Zone Invalidation", options = ["Wick", "Close"],  group = "General Configuration", display = display.none)
combineSDs = DEBUG ? input.bool(true, "Combine Zones", group = "General Configuration", display = display.none) : true
momentumBodyMult = DEBUG ? input.float(0.5, "Momentum Body Mult", step = 0.1, group = "General Configuration") : 0.5
momentumCount = DEBUG ? input.int(4,"Momentum Count", group = "General Configuration") : 4
momentumSpan = DEBUG ? input.int(4, "Momentum Span", group = "General Configuration") : 4
//zoneCount = input.string("High", 'Zone Count', options = ["High", "Medium", "Low", "One"], tooltip = "Number of S&D Zones to be rendered. Higher options will result in older S&Ds shown.",  group = "General Configuration", display = display.none)
zoneCount = "High"
retestsEnabled  = input.bool(true, "Retests", inline = "rb", group = "General Configuration", display = display.none)
breaksEnabled   = input.bool(false, "Breaks", inline = "rb", group = "General Configuration", display = display.none)
showInvalidated = input.bool(true, "Show Historic Zones", group = "General Configuration", display = display.none)
bullSDZoneColor = input(#08998180, 'Demand', inline = 'sdColor', group = 'General Configuration', display = display.none)
bearSDZoneColor = input(#f2364680, 'Supply', inline = 'sdColor', group = 'General Configuration', display = display.none)

demandZones = zoneCount == "One" ? 1 : zoneCount == "Low" ? 3 : zoneCount == "Medium" ? 5 : 30
supplyZones = zoneCount == "One" ? 1 : zoneCount == "Low" ? 3 : zoneCount == "Medium" ? 5 : 30

timeframe1Enabled = input.bool(true, title = "", group = "Timeframes", inline = "timeframe1", display = display.none)
timeframe1 = input.timeframe("", title = "", group = "Timeframes", inline = "timeframe1", display = display.none)
timeframe2Enabled = input.bool(false, title = "", group = "Timeframes", inline = "timeframe2", display = display.none)
timeframe2 = input.timeframe("15", title = "", group = "Timeframes", inline = "timeframe2", display = display.none)
timeframe3Enabled = input.bool(false, title = "", group = "Timeframes", inline = "timeframe3", display = display.none)
timeframe3 = input.timeframe("30", title = "", group = "Timeframes", inline = "timeframe3", display = display.none)

textColor = input.color(#ffffffcc, "Text Color", group = "Style")
labelsAtSameLevel   = DEBUG ? input.bool(true, "[DBG] Place Labels At Same Level", group = "Style") : true
labelsAtSameLevelBreak = false

atr = ta.atr(20)
averageBodySize = ta.sma(math.abs(close - open), 20)

maxDistanceToLastBar := maxDistanceString == "Low" ? 150 : maxDistanceString == "Normal" ? 500 : 1250

type sdZoneInfo
    float top
    float bottom
    string sdType
    int startTime
    int breakTime
    int guid
    string timeframeStr
    bool disabled = false
    string combinedTimeframesStr = na
    bool combined = false

type sdZone
    sdZoneInfo info
    bool isRendered = false

    box sdBox = na

    line sdBoxLineTop = na
    line sdBoxLineMiddle = na
    line sdBoxLineBottom = na
    //
    box sdBoxText = na

type retestLabelContainer
    int guid
    array<label> labels

createSDZone (sdZoneInfo sdZoneInfoF) =>
    sdZone newSDZone = sdZone.new(sdZoneInfoF)
    newSDZone

safeDeleteSDZone (sdZone sdZoneF) =>
    sdZoneF.isRendered := false

    box.delete(sdZoneF.sdBox)
    box.delete(sdZoneF.sdBoxText)

    line.delete(sdZoneF.sdBoxLineTop)
    line.delete(sdZoneF.sdBoxLineMiddle)
    line.delete(sdZoneF.sdBoxLineBottom)

type timeframeInfo
    int index = na
    string timeframeStr = na
    bool isEnabled = false

    sdZoneInfo[] demandZonesList = na
    sdZoneInfo[] supplyZonesList = na

newTimeframeInfo (index, timeframeStr, isEnabled) =>
    newTFInfo = timeframeInfo.new()
    newTFInfo.index := index
    newTFInfo.isEnabled := isEnabled
    newTFInfo.timeframeStr := timeframeStr

    newTFInfo

// ____ TYPES END ____

var timeframeInfo[] timeframeInfos = array.from(newTimeframeInfo(1, timeframe1, timeframe1Enabled), newTimeframeInfo(2, timeframe2, timeframe2Enabled), newTimeframeInfo(3, timeframe3, timeframe3Enabled))
var demandZonesList = array.new<sdZoneInfo>(0)
var supplyZonesList = array.new<sdZoneInfo>(0)
var breakLabels = map.new<int, label>()
var retestLabels = map.new<int, retestLabelContainer>()

var int oldestBarTime = na
if bar_index == last_bar_index - maxDistanceToLastBar
    oldestBarTime := time

var allSDZonesList = array.new<sdZone>(0)

moveLine(_line, _x, _y, _x2) =>
    line.set_xy1(_line, _x,  _y)
    line.set_xy2(_line, _x2, _y)

moveBox (_box, _topLeftX, _topLeftY, _bottomRightX, _bottomRightY) =>
    box.set_lefttop(_box, _topLeftX, _topLeftY)
    box.set_rightbottom(_box, _bottomRightX, _bottomRightY)

isTimeframeLower (timeframe1F, timeframe2F) =>
    timeframe.in_seconds(timeframe1F) < timeframe.in_seconds(timeframe2F)

getMinTimeframe (timeframe1F, timeframe2F) =>
    if isTimeframeLower(timeframe1F, timeframe2F)
        timeframe1F
    else
        timeframe2F

getMaxTimeframe (timeframe1F, timeframe2F) =>
    if isTimeframeLower(timeframe1F, timeframe2F)
        timeframe2F
    else
        timeframe1F

formatTimeframeString (formatTimeframe) =>
    timeframeF = formatTimeframe == "" ? timeframe.period : formatTimeframe
    
    if str.contains(timeframeF, "D") or str.contains(timeframeF, "W") or str.contains(timeframeF, "S") or str.contains(timeframeF, "M")
        timeframeF
    else
        seconds = timeframe.in_seconds(timeframeF)
        if seconds >= 3600
            hourCount = int(seconds / 3600)
            str.tostring(hourCount) + " Hour" + (hourCount > 1 ? "s" : "")
        else
            timeframeF + " Min"

colorWithTransparency (colorF, transparencyX) =>
    color.new(colorF, color.t(colorF) * transparencyX)

createSDBox (boxColor, transparencyX = 1.0, xlocType = xloc.bar_time) =>
    box.new(na, na, na, na, xloc = xlocType, extend = extend.none, bgcolor = colorWithTransparency(boxColor, transparencyX), text_color = textColor, text_halign = text.align_right, text_valign = text.align_bottom, text_size = size.small, border_color = boxColor)

renderSDZone (sdZone sd) =>
    sdZoneInfo info = sd.info
    
    sd.isRendered := true
    
    sdColor = sd.info.sdType == "Demand" ? bullSDZoneColor : bearSDZoneColor

    int zoneSize = na
    if na(info.breakTime)
        zoneSize := (time + 1) - info.startTime
    else
        zoneSize := (info.breakTime - info.startTime)

    render = true
    if zoneSize < timeframe.in_seconds(info.timeframeStr) * minZoneSize * 1000
        render := false
    if info.startTime < nz(oldestBarTime, time)
        render := false


    if render and (showInvalidated or (na(sd.info.breakTime)))
        sd.sdBox := createSDBox(sdColor, 1.5)
        if sd.info.combined
            sd.sdBox.set_bgcolor(colorWithTransparency(sdColor, 1.1))

        startX = info.startTime
        maxEndX = info.startTime + zoneSize / 2

        float middlePoint = (info.top + info.bottom) / 2
        moveBox(sd.sdBox, info.startTime, info.top, info.startTime + zoneSize, info.bottom)
        
        sd.sdBoxLineMiddle := line.new(info.startTime, middlePoint, info.startTime + zoneSize, middlePoint, xloc = xloc.bar_time, color = textColor, style = line.style_dashed)

        sd.sdBoxText := createSDBox(color.new(color.white, 100))
        moveBox(sd.sdBoxText, maxEndX, middlePoint, info.startTime + zoneSize, info.bottom)
        SDText = (na(sd.info.combinedTimeframesStr) ? formatTimeframeString(sd.info.timeframeStr) : sd.info.combinedTimeframesStr) + " " + sd.info.sdType
        //box.set_text(sd.sdBoxText, SDText)
        boxText = na(sd.info.combinedTimeframesStr) ? formatTimeframeString(sd.info.timeframeStr) : sd.info.combinedTimeframesStr
        if DEBUG
            boxText += " | " + str.tostring(sd.info.guid)
        box.set_text(sd.sdBoxText, boxText)
        

areaOfSD (sdZoneInfo SDInfoF) =>
    float XA1 = SDInfoF.startTime
    float XA2 = na(SDInfoF.breakTime) ? time + 1 : SDInfoF.breakTime
    float YA1 = SDInfoF.top
    float YA2 = SDInfoF.bottom
    float edge1 = math.sqrt((XA2 - XA1) * (XA2 - XA1) + (YA2 - YA2) * (YA2 - YA2))
    float edge2 = math.sqrt((XA2 - XA2) * (XA2 - XA2) + (YA2 - YA1) * (YA2 - YA1))
    float totalArea = edge1 * edge2
    totalArea

doSDsTouch (sdZoneInfo SDInfo1, sdZoneInfo SDInfo2) =>
    float XA1 = SDInfo1.startTime
    float XA2 = na(SDInfo1.breakTime) ? (time + 1) : SDInfo1.breakTime
    float YA1 = SDInfo1.top + atr / 100
    float YA2 = SDInfo1.bottom - atr / 100

    float XB1 = SDInfo2.startTime
    float XB2 = na(SDInfo2.breakTime) ? (time + 1) : SDInfo2.breakTime
    float YB1 = SDInfo2.top + atr / 100
    float YB2 = SDInfo2.bottom - atr / 100
    float intersectionArea = math.max(0, math.min(XA2, XB2) - math.max(XA1, XB1)) * math.max(0, math.min(YA1, YB1) - math.max(YA2, YB2))
    float unionArea = areaOfSD(SDInfo1) + areaOfSD(SDInfo2) - intersectionArea
    
    float overlapPercentage = (intersectionArea / unionArea) * 100.0

    if overlapPercentage > overlapThresholdPercentage
        true
    else
        false

isSDValid (sdZoneInfo SDInfo) =>
    valid = true
    if SDInfo.disabled
        valid := false
    valid

clampSDZone (sdZoneInfo sdZoneF) =>
    sdZoneSize = sdZoneF.top - sdZoneF.bottom
    if sdZoneSize > atr * maxZoneSizeATR
        diff = sdZoneSize - (atr * maxZoneSizeATR)
        sdZoneF.top -= diff / 2
        sdZoneF.bottom += diff / 2

combineSDsFunc () =>
    if allSDZonesList.size() > 0
        lastCombinations = 999
        while lastCombinations > 0
            lastCombinations := 0
            for i = 0 to allSDZonesList.size() - 1
                curSD1 = allSDZonesList.get(i)
                for j = 0 to allSDZonesList.size() - 1
                    curSD2 = allSDZonesList.get(j)
                    if i == j
                        continue
                    if not isSDValid(curSD1.info) or not isSDValid(curSD2.info)
                        continue
                    if curSD1.info.sdType != curSD2.info.sdType
                        continue
                    if doSDsTouch(curSD1.info, curSD2.info)
                        curSD1.info.disabled := true
                        curSD2.info.disabled := true

                        sdZone newSD = createSDZone(sdZoneInfo.new(math.max(curSD1.info.top, curSD2.info.top), math.min(curSD1.info.bottom, curSD2.info.bottom), curSD1.info.sdType))
                        newSD.info.startTime := math.min(curSD1.info.startTime, curSD2.info.startTime)
                        newSD.info.breakTime := math.max(nz(curSD1.info.breakTime), nz(curSD2.info.breakTime))
                        newSD.info.breakTime := newSD.info.breakTime == 0 ? na : newSD.info.breakTime
                        newSD.info.guid := newSD.info.startTime
                        newSD.info.timeframeStr := curSD1.info.timeframeStr
                        clampSDZone(newSD.info)
                        
                        newSD.info.combined := true
                        if timeframe.in_seconds(curSD1.info.timeframeStr) != timeframe.in_seconds(curSD2.info.timeframeStr)
                            newSD.info.combinedTimeframesStr := (na(curSD1.info.combinedTimeframesStr) ? formatTimeframeString(curSD1.info.timeframeStr) : curSD1.info.combinedTimeframesStr) + " & " + (na(curSD2.info.combinedTimeframesStr) ? formatTimeframeString(curSD2.info.timeframeStr) : curSD2.info.combinedTimeframesStr)
                        allSDZonesList.unshift(newSD)
                        lastCombinations += 1


reqSeq (timeframeStr) =>
    if timeframe.in_seconds(timeframeStr) == timeframe.in_seconds()
        [demandZonesList, supplyZonesList]
    else
        [demandZonesListF, supplyZonesListF] = request.security(syminfo.tickerid, timeframeStr, [demandZonesList, supplyZonesList])
        [demandZonesListF, supplyZonesListF]

getTFData (timeframeInfo timeframeInfoF, timeframeStr) =>
    if timeframeInfoF.isEnabled
        [demandZonesListF, supplyZonesListF] = reqSeq(timeframeStr)
        [demandZonesListF, supplyZonesListF]
    else
        [na, na]

handleTimeframeInfo (timeframeInfo timeframeInfoF, demandZonesListF, supplyZonesListF) =>
    if timeframeInfoF.isEnabled
        timeframeInfoF.demandZonesList := demandZonesListF
        timeframeInfoF.supplyZonesList := supplyZonesListF

handleSDZonesFinal () =>
    if DEBUG
        log.info("Demand Count " + str.tostring(demandZonesList.size()))
        log.info("Supply Count " + str.tostring(supplyZonesList.size()))
        log.info("All " + str.tostring(allSDZonesList.size()))
        log.info("Max " + str.tostring(demandZones))

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            safeDeleteSDZone(allSDZonesList.get(i))
    allSDZonesList.clear()    

    for i = 0 to timeframeInfos.size() - 1
        curTimeframe = timeframeInfos.get(i)
        if not curTimeframe.isEnabled
            continue
        if curTimeframe.demandZonesList.size() > 0
            for j = 0 to math.min(curTimeframe.demandZonesList.size() - 1, demandZones - 1)
                sdZoneInfoF = curTimeframe.demandZonesList.get(j)
                sdZoneInfoF.timeframeStr := curTimeframe.timeframeStr
                allSDZonesList.unshift(createSDZone(sdZoneInfo.copy(sdZoneInfoF)))

        if curTimeframe.supplyZonesList.size() > 0
            for j = 0 to math.min(curTimeframe.supplyZonesList.size() - 1, supplyZones - 1)
                sdZoneInfoF = curTimeframe.supplyZonesList.get(j)
                sdZoneInfoF.timeframeStr := curTimeframe.timeframeStr
                allSDZonesList.unshift(createSDZone(sdZoneInfo.copy(sdZoneInfoF)))

    if combineSDs
        combineSDsFunc()

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curSD = allSDZonesList.get(i)
            if isSDValid(curSD.info)
                renderSDZone(curSD)

bodySize = math.abs(close - open)
getMomentumCandleCount (lastBars, reqMult) =>
    bearishCnt = 0
    bullishCnt = 0
    for i = 0 to lastBars - 1
        if bodySize[i] >= averageBodySize * reqMult
            if close[i] > open[i]
                bullishCnt += 1
            else
                bearishCnt += 1
    [bullishCnt, bearishCnt]

[bullishMomentum, bearishMomentum] = getMomentumCandleCount(momentumSpan, momentumBodyMult)

var int lastDemandZone = 0
var int lastSupplyZone = 0
// Find Supply & Demand
if bar_index > last_bar_index - maxDistanceToLastBar
    if bullishMomentum >= momentumCount and bar_index - lastDemandZone > minDistanceBetweenZones
        lastDemandZone := bar_index
        newSDZone = sdZoneInfo.new(high[momentumSpan + 1], low[momentumSpan + 1], "Demand", time[momentumSpan + 1], na, time[momentumSpan + 1])
        clampSDZone(newSDZone)
        demandZonesList.unshift(newSDZone)
        if demandZonesList.size() > maxSDZones
            demandZonesList.pop()
    if bearishMomentum >= momentumCount and bar_index - lastSupplyZone > minDistanceBetweenZones
        lastSupplyZone := bar_index
        newSDZone = sdZoneInfo.new(high[momentumSpan + 1], low[momentumSpan + 1], "Supply", time[momentumSpan + 1], na, time[momentumSpan + 1])
        clampSDZone(newSDZone)
        supplyZonesList.unshift(newSDZone)
        if supplyZonesList.size() > maxSDZones
            supplyZonesList.pop()

    // Invalidation
    if demandZonesList.size() > 0
        for i = demandZonesList.size() - 1 to 0
            currentSD = demandZonesList.get(i)
        
            if na(currentSD.breakTime) 
                if (sdEndMethod == "Wick" ? low : math.min(open, close)) < currentSD.bottom
                    currentSD.breakTime := time

    if supplyZonesList.size() > 0
        for i = supplyZonesList.size() - 1 to 0
            currentSD = supplyZonesList.get(i)

            if na(currentSD.breakTime) 
                if (sdEndMethod == "Wick" ? high : math.max(open, close)) > currentSD.top
                    currentSD.breakTime := time

[demandZonesListTimeframe1, supplyZonesListTimeframe1] = getTFData(timeframeInfos.get(0), timeframe1)
[demandZonesListTimeframe2, supplyZonesListTimeframe2] = getTFData(timeframeInfos.get(1), timeframe2)
[demandZonesListTimeframe3, supplyZonesListTimeframe3] = getTFData(timeframeInfos.get(2), timeframe3)

var lastRetestIndexSupply = 0
var lastRetestIndexDemand = 0

float renderRetestLabelBuyside = na
int renderRetestLabelBuysideGUID = na

float renderRetestLabelSellside = na
int renderRetestLabelSellsideGUID = na

float renderBreakLabelBuyside = na
int renderBreakLabelBuysideGUID = na

float renderBreakLabelSellside = na
int renderBreakLabelSellsideGUID = na

var disabledDuplicateTF = false
// Disable Duplicate Timeframes
if not disabledDuplicateTF
    disabledDuplicateTF := true
    for i = 0 to timeframeInfos.size() - 1
        for j = 0 to timeframeInfos.size() - 1
            if i == j
                continue
            timeframeInfo1 = timeframeInfos.get(i)
            timeframeInfo2 = timeframeInfos.get(j)
            if timeframeInfo1.isEnabled and timeframeInfo2.isEnabled and timeframe.in_seconds(timeframeInfo1.timeframeStr) == timeframe.in_seconds(timeframeInfo2.timeframeStr)
                timeframeInfo1.isEnabled := false

if barstate.isconfirmed and bar_index > last_bar_index - maxDistanceToLastBar
    handleTimeframeInfo(timeframeInfos.get(0), demandZonesListTimeframe1, supplyZonesListTimeframe1)
    handleTimeframeInfo(timeframeInfos.get(1), demandZonesListTimeframe2, supplyZonesListTimeframe2)
    handleTimeframeInfo(timeframeInfos.get(2), demandZonesListTimeframe3, supplyZonesListTimeframe3)
    handleSDZonesFinal()

    // Breaks    

    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curZone = allSDZonesList.get(i)
            if curZone.info.disabled
                continue
            if not showInvalidated and not na(curZone.info.breakTime)
                continue
            if na(curZone.info.breakTime)
                continue
            if time - curZone.info.startTime < minZoneSize * timeframe.in_seconds(curZone.info.timeframeStr) * 1000
                continue
            if curZone.info.startTime < nz(oldestBarTime, time)
                continue
            
            if time == curZone.info.breakTime
                if curZone.info.sdType == "Supply"
                    if curZone.info.breakTime - curZone.info.startTime > minZoneSize * timeframe.in_seconds() * 1000
                        renderBreakLabelBuyside := curZone.info.bottom
                        renderBreakLabelBuysideGUID := curZone.info.guid
                else
                    if curZone.info.breakTime - curZone.info.startTime > minZoneSize * timeframe.in_seconds() * 1000
                        renderBreakLabelSellside := curZone.info.top
                        renderBreakLabelSellsideGUID := curZone.info.guid
    
    // Retests
    if allSDZonesList.size() > 0
        for i = 0 to allSDZonesList.size() - 1
            curZone = allSDZonesList.get(i)
            
            if curZone.info.disabled
                continue
            if not showInvalidated and not na(curZone.info.breakTime)
                continue
            if not na(curZone.info.breakTime)
                continue
            if time - curZone.info.startTime < minZoneSize * timeframe.in_seconds(curZone.info.timeframeStr) * 1000
                continue
            if curZone.info.startTime < nz(oldestBarTime, time)
                continue
            
            middleLine = (curZone.info.bottom + curZone.info.top) / 2.0
            if curZone.info.sdType == "Supply" and bar_index - lastRetestIndexSupply > RETEST_COOLDOWN
                if high > curZone.info.bottom
                    renderRetestLabelBuyside := curZone.info.top
                    renderRetestLabelBuysideGUID := curZone.info.guid
                    lastRetestIndexSupply := bar_index
            else if curZone.info.sdType == "Demand" and bar_index - lastRetestIndexDemand > RETEST_COOLDOWN
                if low < curZone.info.top
                    renderRetestLabelSellside := curZone.info.bottom
                    renderRetestLabelSellsideGUID := curZone.info.guid
                    lastRetestIndexDemand := bar_index

//plotshape(not na(renderRetestLabelBuyside) and retestsEnabled ? renderRetestLabelBuyside : na, "", shape.labeldown, color = bearSDZoneColor, text = "R", location = labelsAtSameLevel ? location.absolute : location.abovebar, textcolor = color.white, size = size.small)
//plotshape(not na(renderRetestLabelSellside) and retestsEnabled ? renderRetestLabelSellside : na, "", shape.labelup, color = bullSDZoneColor, text = "R", location = labelsAtSameLevel ? location.absolute : location.belowbar, textcolor = color.white, size = size.small)

// Retests

if not na(renderRetestLabelBuyside) and retestsEnabled
    newLabel = label.new(bar_index, renderRetestLabelBuyside, style = label.style_label_down, color = bearSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    //label.new(bar_index, renderRetestLabelSellside, style = label.style_label_up, color = bullSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    if na(retestLabels.get(renderRetestLabelBuysideGUID))
        newContainer = retestLabelContainer.new(renderRetestLabelBuysideGUID)
        newContainer.labels := array.new<label>()
        newContainer.labels.push(newLabel)
        retestLabels.put(renderRetestLabelBuysideGUID, newContainer)
    else
        retestLabels.get(renderRetestLabelBuysideGUID).labels.push(newLabel)

if not na(renderRetestLabelSellside) and retestsEnabled
    newLabel = label.new(bar_index, renderRetestLabelSellside, style = label.style_label_up, color = bullSDZoneColor, text = "R", textcolor = color.white, size = size.small)
    if na(retestLabels.get(renderRetestLabelSellsideGUID))
        newContainer = retestLabelContainer.new(renderRetestLabelSellsideGUID)
        newContainer.labels := array.new<label>()
        newContainer.labels.push(newLabel)
        retestLabels.put(renderRetestLabelSellsideGUID, newContainer)
    else
        retestLabels.get(renderRetestLabelSellsideGUID).labels.push(newLabel)


if retestLabels.keys().size() > 0
    for i = 0 to retestLabels.keys().size() - 1
        curKey = retestLabels.keys().get(i)
        foundKey = false
        if allSDZonesList.size() > 0
            for j = 0 to allSDZonesList.size() - 1
                if allSDZonesList.get(j).info.guid == curKey
                    if allSDZonesList.get(j).info.disabled
                        continue
                    if not showInvalidated and not na(allSDZonesList.get(j).info.breakTime)
                        continue
                    if time - allSDZonesList.get(j).info.startTime < minZoneSize * timeframe.in_seconds(allSDZonesList.get(j).info.timeframeStr) * 1000
                        continue
                    if allSDZonesList.get(j).info.startTime < nz(oldestBarTime, time)
                        continue
                    foundKey := true
                    break
        if not foundKey
            for j = 0 to retestLabels.get(curKey).labels.size() - 1
                label.delete(retestLabels.get(curKey).labels.get(j))

// Breaks
if not na(renderBreakLabelBuyside) and breaksEnabled
    breakLabels.put(renderBreakLabelBuysideGUID, label.new(bar_index, renderBreakLabelBuyside, style = label.style_label_up, color = color.blue, text = "B", textcolor = color.white, size = size.small))

if not na(renderBreakLabelSellside) and breaksEnabled
    breakLabels.put(renderBreakLabelSellsideGUID, label.new(bar_index, renderBreakLabelSellside, style = label.style_label_down, color = color.blue, text = "B", textcolor = color.white, size = size.small))

if breakLabels.keys().size() > 0
    for i = 0 to breakLabels.keys().size() - 1
        curKey = breakLabels.keys().get(i)
        foundKey = false
        if allSDZonesList.size() > 0
            for j = 0 to allSDZonesList.size() - 1
                if allSDZonesList.get(j).info.guid == curKey
                    if allSDZonesList.get(j).info.disabled
                        continue
                    foundKey := true
                    break
        if not foundKey
            label.delete(breakLabels.get(curKey))

alertcondition(not na(renderRetestLabelBuyside) and barstate.isconfirmed, "Supply Zone Retest @ {{ticker}}", "Supply Zone Retest @ {{ticker}}")
alertcondition(not na(renderRetestLabelSellside) and barstate.isconfirmed, "Demand Zone Retest @ {{ticker}}", "Demand Zone Retest @ {{ticker}}")

alertcondition(not na(renderBreakLabelBuyside) and barstate.isconfirmed, "Supply Zone Break @ {{ticker}}", "Supply Zone Break @ {{ticker}}")
alertcondition(not na(renderBreakLabelSellside) and barstate.isconfirmed, "Demand Zone Break @ {{ticker}}", "Demand Zone Break @ {{ticker}}")
```