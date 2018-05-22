package com.apo.ncc;

import com.intellij.execution.ExecutionException;
import com.intellij.execution.configurations.CommandLineState;
import com.intellij.execution.configurations.GeneralCommandLine;
import com.intellij.execution.process.KillableColoredProcessHandler;
import com.intellij.execution.process.OSProcessHandler;
import com.intellij.execution.process.ProcessHandler;
import com.intellij.execution.process.ProcessTerminatedListener;
import com.intellij.execution.runners.ExecutionEnvironment;
import org.jetbrains.annotations.NotNull;

class NccCommandLineState extends CommandLineState {
    private final NccRunConfiguration runConfig;

    NccCommandLineState(NccRunConfiguration runConfig, ExecutionEnvironment environment) {
        super(environment);
        this.runConfig = runConfig;
    }

    @NotNull
    @Override
    protected ProcessHandler startProcess() throws ExecutionException {

        GeneralCommandLine cmd = new GeneralCommandLine();
        cmd.setExePath(runConfig.getPython3Path()); //python
        cmd.addParameter(runConfig.getInterpreterPath()); //main.py
        cmd.addParameter(runConfig.getScriptName()); //script file
        cmd.getParametersList().addParametersString(runConfig.getProgramParameters()); //script parameters

        OSProcessHandler processHandler = new KillableColoredProcessHandler(cmd);
        ProcessTerminatedListener.attach(processHandler, getEnvironment().getProject());

        return processHandler;
    }
}
