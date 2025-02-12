class Apple {
    public void show() {
        System.out.println("show() method of Apple  ");
    }
}

class Banana extends Apple {
    @Override
    public void show() {
        System.out.println("show() method of Banana  ");
    }
}

class Cherry extends Apple {
    @Override
    public void show() {
        System.out.println("show() method of Cherry  ");
    }
}

public class q3 {
    public static void main(String[] args) {
        Apple ref;

        ref = new Apple();
        ref.show();

        ref = new Banana();
        ref.show();

        ref = new Cherry();
        ref.show();
    }
}
