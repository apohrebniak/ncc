{ int one = 1
  int N
  in(N)
  if N <= 1 ? { out(N, one)} : {  int factorial = N
                                while [N > 1] do { N = N - 1
                                                   factorial = factorial * N}
                                out(N, factorial)}}