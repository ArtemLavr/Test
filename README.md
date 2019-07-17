# Untested-Levels

The idea is to create a loop inside a loop:

We take [zup], and for each one we create: [zupNumber] [zupFirst] [zupCandle]

The loops are created from each  ['x'] where there is a ['zup'] to the end of the dataset and the check:

[zupNumber] The number of candles that crosed the level

[zupCandle] The ['x'] of the first candle that crossed the level (As you created before: df['high'][x] > df['res'][x-1] and df['high'][x-1] < df['res'][x-1])

[zupFirst] The ['x'] of the second candle wich touched the level by a %: This time we use ['high'] and create a window of 1%:
0.99*['high'])        1.01*['high'] 

An example candle would look as follows:

![alt text](https://raw.githubusercontent.com/eyefate/Untested-Levels/master/untested.png?token=AHEMI5AIFVIJXY3P4YERL525F5QD4)
