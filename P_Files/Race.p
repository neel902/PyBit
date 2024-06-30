frame1 {
    $rdi = $0000;
};
frame2 {
    $rdi = $0001;

    $0111 = $0111 + $1110;
};

left {
    $0011 = $0011 - $0100;
};
right {
    $0011 = $0011 + $0100;
};
summon {
    rndm(random2);
    rndm(random2);
    rndm(random2);
    rndm(random2);
    rndm(random2);
    rndm(random2);
    rndm(random2);
    rndm(random2);

    rndm(random4);
    rndm(random4);
    rndm(random4);
    rndm(random4);

    rndm(random3);
    rndm(random3);

    rndm(random1);
    $0110 = $rdi;
    $0111 = 00000000;
};

tempNest1 {
    $rdi = 01011010;
    if (<, $0111, $rdi, tempNest2);
};

tempNest2 {
    $rdi = 00100010;
    $rax = $0110 - $0011;

    if (<, $rax, $rdi, die);

    $rdi = 00000000;
    $rax = $rdi - $rax;

    if (<, $rax, $rdi, die);
};

die {
    :START "exit";
};

random1 {
    $rdi = 01001011;
};
random2 {
    $rdi = 00111011;
};
random3 {
    $rdi = 01100000;
};
random4 {
    $rdi = 00100000;
};

tick {
    if:even ($clock, frame1);
    if:odd ($clock, frame2);
    image(1, 1);
    $rdi = $0010;
    image($0011, 60);
    key($1111);
    if (@, $1111, $1100, left);
    if (@, $1111, $1101, right);

    $rax = 00000010;
    if (@, $clock, $rax, summon);

    $rdi = $1010;
    image($0110, $0111);

    $rdi = 00111100;
    
    if (>, $0111, $rdi, tempNest1);    
};

// SPIKE X;
$0110 = 01001011;

// SPIKE Y;
$0111 = 00000000;

// SPIKE SPEED;
$1110 = 00000110;

display();
$1100 = 00001011;
$1101 = 00001110;

$0011 = 01001011;
$0100 = 00000100;

$rdi = "/assets/bg/frame1-img";
open();
read();
close();
$0000 = $rdi;
$rdi = "/assets/bg/frame2-img";
open();
read();
close();
$0001 = $rdi;
$rdi = "/assets/car/frame1-img";
open();
read();
close();
$0010 = $rdi;
$rdi = "/assets/spike-img";
open();
read();
close();
$1010 = $rdi;