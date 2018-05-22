package com.apo.ncc;

import com.intellij.execution.CommonProgramRunConfigurationParameters;
import com.intellij.execution.ExecutionException;
import com.intellij.execution.Executor;
import com.intellij.execution.configurations.ConfigurationFactory;
import com.intellij.execution.configurations.RunConfiguration;
import com.intellij.execution.configurations.RunConfigurationBase;
import com.intellij.execution.configurations.RunProfileState;
import com.intellij.execution.configurations.RuntimeConfigurationException;
import com.intellij.execution.runners.ExecutionEnvironment;
import com.intellij.openapi.options.SettingsEditor;
import com.intellij.openapi.project.Project;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.LinkedHashMap;
import java.util.Map;

public class NccRunConfiguration extends RunConfigurationBase implements CommonProgramRunConfigurationParameters {

    private String python3Path = "/usr/bin/python3";
    private String interpreterPath = "";
    private String scriptName;
    private String scriptParameters;
    private String workingDirectory = "";

    protected NccRunConfiguration(Project project, ConfigurationFactory factory, String name) {
        super(project, factory, name);
    }

    @NotNull
    @Override
    public SettingsEditor<? extends RunConfiguration> getConfigurationEditor() {
        return new NccSettingsEditor();
    }

    @Override
    public void checkConfiguration() throws RuntimeConfigurationException {

    }

    @Nullable
    @Override
    public RunProfileState getState(@NotNull Executor executor, @NotNull ExecutionEnvironment executionEnvironment) throws ExecutionException {
        return new NccCommandLineState(this, executionEnvironment);
    }

    public String getInterpreterPath() {
        return this.interpreterPath;
    }

    public void setInterpreterPath(String interpreterPath) {
        this.interpreterPath = interpreterPath;
    }

    public String getScriptName() {
        return this.scriptName;
    }

    public void setScriptName(String scriptName) {
        this.scriptName = scriptName;
    }

    public String getPython3Path() {
        return python3Path;
    }

    public void setPython3Path(String python3Path) {
        this.python3Path = python3Path;
    }

    @Override
    public void setProgramParameters(@Nullable String s) {
        scriptParameters = s;
    }

    @Nullable
    @Override
    public String getProgramParameters() {
        return scriptParameters;
    }

    @Override
    public void setWorkingDirectory(@Nullable String s) {
        workingDirectory = s;
    }

    @Nullable
    @Override
    public String getWorkingDirectory() {
        return workingDirectory;
    }

    @Override
    public void setEnvs(@NotNull Map<String, String> map) {

    }

    @NotNull
    @Override
    public Map<String, String> getEnvs() {
        return new LinkedHashMap<>();
    }

    @Override
    public void setPassParentEnvs(boolean b) {

    }

    @Override
    public boolean isPassParentEnvs() {
        return false;
    }
}
