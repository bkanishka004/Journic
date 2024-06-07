gsap.to("#nav", {
  backgroundColor: "#000",
  duration: 0.2,
  height: "110px",
  scrollTrigger: {
    trigger: "#nav",
    scroller: "body",
    start: "top -10%",
    end: "top -11%",
    scrub: 1,
  },
});

gsap.to("#main", {
  backgroundColor: "#000",
  scrollTrigger: {
    trigger: "#main",
    scroller: "body",
    start: "top -25%",
    end: "top -70%",
    scrub: 2,
  },
});

gsap.from("#about-us img,#about-us-in", {
  y: 90,
  opacity: 0,
  duration: 1,
  scrollTrigger: {
    trigger: "#about-us",
    scroller: "body",

    start: "top 90%",
    end: "top 5%",
    scrub: 1,
  },
});
gsap.from(".card", {
  scale: 0.8,

  duration: 1,
  stagger: 0.1,
  scrollTrigger: {
    trigger: ".card",
    scroller: "body",

    start: "top 70%",
    end: "top 65%",
    scrub: 1,
  },
});
