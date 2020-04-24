# double不能参与乘，除运算,请用BigDecimal,BigInteger
金额从19.9===>19.89了。。
```java
public class CurrencyUtilTest {
    @Test
    public void test() {
        double priceYuan = BigDecimal.valueOf(19.9).doubleValue();
        //error
        double priceFen = priceYuan * 100;
        System.out.println(priceYuan + "," + priceFen);
        int fen = (int) (priceFen * 100);
        System.out.println(fen);
        BigDecimal multiply = BigDecimal.valueOf(19.9).multiply(BigDecimal.valueOf(100));

        System.out.println(multiply + "," + multiply.intValue());
    }
}
```
乘之后华丽丽的丢了一分钱
```
19.9,1989.9999999999998
198999
1990.0,1990
```