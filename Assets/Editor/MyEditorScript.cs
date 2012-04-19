class MyEditorScript
{
	/* standard */
	static void PerformMacOSXBuild () {
	}

	/* some spaces */
	[MenuItem ("Custom/CI/Build FlashPlayer")]
	public     static    void   PerformFlashBuild ( )
	{
	}

	/* we pick method even if brackets are on same line */
	static void PerformWin32Build () {
	}

	/* methods with arguments should be ignored */
	static void PerformGenericWindowsBuild (string _WinType, BuildTarget _BuildTarget)
	{
	}
/* method whose declaration is over several lines are also ignored */
[MenuItem ("Custom/CI/Build iOS")]
static 
void PerformIOSBuild ()
	{   
	}

/* method that return something else than void are ignored */
	private static string[] IgnoredNonVoidMethods()
	{
	}
	/* internal methods are ignored */
	internal static void IgnoredPerformBuildInternal1 () {
	}
	static internal void IgnoredPerformBuildInternal2 () {
	}

	/* private methods are ignored */
	private static string IgnoredPerformBuildInternal () {
	}
		
	/* private methods are ignored */
	static private string IgnoredPerformBuildInternal () {
	}

	static void Zip(string _TargetFileOrDirName, string _BundleName)
	{   
	}
}
