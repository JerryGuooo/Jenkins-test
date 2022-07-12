@RestController
public class Hello {

    @RequestMapping("/")
    public String sayHello(){
	    //修改返回的字符串的内容
        return "abcdefg. Hello jenkins, " + new Date();
    }
}
