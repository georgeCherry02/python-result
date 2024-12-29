from result import Result

def main():
    temp = Result[int, str].Ok(5)
    t2 = temp.map(lambda x: x + 1) \
        .map_err(lambda s: f"err:{s}") \
        .and_then(lambda c: Result[str, str].Err(f"Oh no..., init={c}")) \
        .map_err(lambda s: f"propagate and mutate: {s}")
    print(t2)

if __name__ == "__main__":
    main()
