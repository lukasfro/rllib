"""Python Script Template."""

from exps.gpucrl.util import parse_results, print_df

base_dir = 'runs/Cartpoleenv'
for agent in ['MPC', 'MBMPPO']:
    df = parse_results(base_dir, agent)
    print(agent)
    print_df(df, idx=19)

    df.to_pickle(f'./{agent}.pk')