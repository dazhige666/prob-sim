from prob_sim.ks import simulate

def main() -> None:
    xs = simulate(50, 2000,42)
    assert all(0.0 <= d <= 1.0 for d in xs)


    sorted_xs = sorted(xs)
    if len(xs) % 2 == 0:
        median = (sorted_xs[len(xs)//2] + sorted_xs[len(xs)//2 - 1]) / 2
    else:
        median = sorted_xs[len(xs)//2]
    assert (0.117 * 0.7 <= median <= 0.117 * 1.3)


    xs1 = simulate(50, 2000,42)
    xs2 = simulate(50, 2000,42)
    assert xs1 == xs2,"同seed结果不一致"

    print("all passed")

if __name__ == "__main__":
    main()