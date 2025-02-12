interface Salary{
    void earnings();
    void deductions();
    void bonus();
}

abstract class Manager implements Salary{
    double basic;
    public Manager(double basic){
        this.basic = basic;
    }
    @Override
    public void earnings(){
        double da = basic * 0.8;
        double hra = basic * 0.15;
        double totalEarnings = basic + da + hra;
        System.out.println("Earnings - " + totalEarnings);
    }
    @Override
    public void deductions(){
        double pf = basic * 0.12;
        System.out.println("Deduction - " + pf);
    }
}

class Substaff extends Manager{
    public Substaff(double basic){
        super(basic);
    }
    @Override
    public void bonus(){
        double bonus = basic * 0.5;
        System.out.println("Bonus - " + bonus);
    }
}

public class q3 {
    public static void main(String[] args) {
        Substaff s = new Substaff(50000);
        System.out.println("Basic - " + s.basic); 
        s.earnings();
        s.deductions();
        s.bonus();
    }
}