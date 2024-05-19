frame1 {
    $rdi = $0000;
};
frame2 {
    $rdi = $0001;
};
left {
    $0011 = $0011 - $0100;
};
right {
    $0011 = $0011 + $0100;
};
tick {
    if:even ($clock, frame1);
    if:odd ($clock, frame2);
    image(1, 1);
    $rdi = $0010;
    image($0011, 60);
    key($1111);
    if ($1111 @ $1100, left);
    if ($1111 @ $1101, right);
};
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
