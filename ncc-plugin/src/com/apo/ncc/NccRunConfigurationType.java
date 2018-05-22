package com.apo.ncc;

import com.intellij.execution.configurations.ConfigurationFactory;
import com.intellij.execution.configurations.ConfigurationType;
import com.intellij.icons.AllIcons;
import org.jetbrains.annotations.NotNull;

import javax.swing.*;

public class NccRunConfigurationType implements ConfigurationType {
    @Override
    public String getDisplayName() {
        return "NCC";
    }

    @Override
    public String getConfigurationTypeDescription() {
        return "Run NCC";
    }

    @Override
    public Icon getIcon() {
        return AllIcons.General.Information;
    }

    @NotNull
    @Override
    public String getId() {
        return "NCC_RUN_CONFIGURATION";
    }

    @Override
    public ConfigurationFactory[] getConfigurationFactories() {
        return new ConfigurationFactory[]{new NccConfigurationFactory(this)};
    }
}
