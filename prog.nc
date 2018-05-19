{ float N
  in(N)
  if N <= 1 ? { out(N)} : {  float factorial = N
                                while [N > 1] do { N = N - 1
                                                   factorial = factorial * N}
                                out(factorial)}}